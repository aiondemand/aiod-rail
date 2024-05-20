import { FlatTreeControl } from '@angular/cdk/tree';
import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { MatTreeFlatDataSource, MatTreeFlattener } from '@angular/material/tree';
import { Observable, Subscription, catchError, firstValueFrom, interval, mergeMap, of, retry, switchMap, tap } from 'rxjs';
import { Experiment } from 'src/app/models/experiment';
import { ExperimentRunDetails } from 'src/app/models/experiment-run';
import { FileDetail } from 'src/app/models/file-detail';
import { ConfirmPopupInput, ConfirmPopupResponse } from 'src/app/models/popup';
import { BackendApiService } from 'src/app/services/backend-api.service';
import { SnackBarService } from 'src/app/services/snack-bar.service';
import { ConfirmPopupComponent } from '../../general/popup/confirm-popup.component';
import { MatDialog } from '@angular/material/dialog';

interface FileNode {
  name: string;
  filepath: string;
  last_modified?: string;
  size?: number;
  children?: FileNode[];
}

interface FlattenedNode {
  node: FileNode;
  name: string;
  expandable: boolean;
  level: number;
}

@Component({
  selector: 'app-experiment-run-detail',
  templateUrl: './experiment-run-detail.component.html',
  styleUrls: ['./experiment-run-detail.component.scss']
})
export class ExperimentRunDetailComponent {
  experiment: Experiment;
  
  fileTreeStructure: FileNode[] = [];
  treeControl: FlatTreeControl<FlattenedNode> | null = null;
  treeViewDataSource: MatTreeFlatDataSource<FileNode, FlattenedNode> | null = null;

  currentlyBeingDownloaded = new Set<string>();

  @Input()
  set runId(id: string) {
    this.subscription = this.backend.getExperimentRun(id).pipe(
      switchMap(run => {
        firstValueFrom(this.backend.getExperiment(run.experiment_id))
          .then(exp => this.experiment = exp)
          .catch(err => console.error(err));

        if (run.state == 'CREATED' || run.state == 'IN_PROGRESS') {
          this.experimentRun = run;
          return interval(5000).pipe(switchMap(_ => this.backend.getExperimentRun(id)));
        }
        else {
          return of(run);
        }
      }),
    ).subscribe({
      next: run => {
        this.experimentRun = run;

        if (this.experimentRun.logs) {
          let logs = JSON.parse(this.experimentRun.logs)["job_logs"];
          let key = Object.keys(logs)[0];
          this.logs = logs[key]["logs"];
        }
        else {
          this.logs == '';
        }

        if (run.state != 'CREATED' && run.state != 'IN_PROGRESS') {
          this.subscription.unsubscribe();

          firstValueFrom(this.backend.listFilesFromExperimentRun(run.id))
            .then(files => {
              this.buildTreeFileStructure(files);

              this.treeControl = new FlatTreeControl<FlattenedNode>(
                node => node.level,
                node => node.expandable,
              );
            
              let treeFlattener = new MatTreeFlattener(
                this.flattenNode,
                node => node.level,
                node => node.expandable,
                node => node.children,
              );
            
              this.treeViewDataSource = new MatTreeFlatDataSource(this.treeControl, treeFlattener);
              this.treeViewDataSource.data = this.fileTreeStructure;
            })
            .catch(err => console.error(err))
        }
      },
      error: err => {
        this.snackBar.showError(`Couldn't load experiment run: ${err.message}`);
      }
    });
  }

  downloadfile(event: Event, filepath: string) { 
    event.stopPropagation();
    this.currentlyBeingDownloaded.add(filepath);

    // TODO make this less ugly
    this.backend.downloadFileFromExperimentRun(this.experimentRun.id, filepath).subscribe(response => {
      let blobObj = new Blob([response.body], { type: response.body.type });
      let url = window.URL.createObjectURL(blobObj);
      let link = document.createElement('a');
      
      let filename = response.headers
        .get('content-disposition')
        .split('filename=')[1]
        .split(';')[0]
      let first_quote = filename[0]
      let last_quote_idx = filename.slice(1).indexOf(first_quote)
      filename = filename.slice(1, 1+last_quote_idx);

      link.href = url;
      link.download = filename;
      link.style.display = 'none';
      document.body.appendChild(link);
      link.click();

      window.URL.revokeObjectURL(url);
      document.body.removeChild(link);

      this.currentlyBeingDownloaded.delete(filepath);
    });
      
  }

  sortFilesFunction(x: string, y: string): number {
    if (x.endsWith("/") && !y.endsWith("/")) {
      return -1;
    }
    if (!x.endsWith("/") && y.endsWith("/")) {
      return 1;
    }
    if (x < y) {
      return -1;
    }
    if (x > y) {
      return 1;
    }
    return 0;  
  }

  buildTreeFileStructure(files: FileDetail[]): void {
    for (let file of files) {
      let parts = file.filepath.split("/");
      let nodeTraverser: FileNode[] = this.fileTreeStructure;
      for (let it = 0; it < parts.length; it++) {
        let filename = parts[it]
        let filepath = parts.slice(0, it+1).join("/");
        let nameArr = nodeTraverser.map(node => node.name);
  
        if (it == parts.length - 1) {
          // file
          if (nodeTraverser.findIndex(node => node.filepath == filepath) == -1) {
            nameArr.push(filename);
            let idxToPush = nameArr.sort(this.sortFilesFunction).indexOf(filename);

            nodeTraverser.splice(idxToPush, 0, {
              name: filename,
              filepath: file.filepath,
              last_modified: file.last_modified,
              size: file.size
            });
          }
        }
        else {
          // directory
          let idx = nodeTraverser.findIndex(node => node.filepath == filepath)
          if (idx == -1) {
            filename = `${filename}/`;
            nameArr.push(filename);
            let idxToPush = nameArr.sort(this.sortFilesFunction).indexOf(filename);
            
            let newDir = {
              name: filename,
              filepath: filepath,
              children: []
            };
            nodeTraverser.splice(idxToPush, 0, newDir);
            nodeTraverser = newDir.children;
          }
          else {
            nodeTraverser = nodeTraverser[idx].children ?? []
          }
        }
      }
    } 
  }

  flattenNode(node: FileNode, level: number) {
    return {
      node: node,
      name: node.name,
      expandable: !!node.children && node.children.length > 0,
      level: level,
    }
  }

  hasChild = (_: number, node: FlattenedNode) => node.expandable;

  formatFileSize(size: number): string {
    let sizes_abbr = ["B", "KB", "MB", "GB"]
    
    for (let abbr of sizes_abbr) {
      if (size < 1024) {
        size = Math.round(size * 100) / 100
        return `${size} ${abbr}`;
      }
      size /= 1024;
    }
    size = Math.round(size * 100) / 100
    return `${size} TB`;
  }

  ngOnDestroy() {
    this.subscription?.unsubscribe();
  }

  logs: string = "";

  experimentRun: ExperimentRunDetails;
  subscription: Subscription;

  constructor(
    private backend: BackendApiService,
    private snackBar: SnackBarService,
    private dialog: MatDialog,
  ) { }

  wandbLink(logs: string | null): string {
    if (!logs) return '';

    // regex to match https://wandb.ai/WANDB_ENTITY/aiod-demo/runs/RUN_ID
    const regex = /https:\/\/wandb.ai\/(.*)\/(.*)\/runs\/(.*)/g;
    const match = regex.exec(logs);
    if (match) {
      return match[0];
    }
    else {
      return '';
    }
  }

  getRunNameFromWandBLink(link: string): string {
    const regex = /https:\/\/wandb.ai\/(.*)\/(.*)\/runs\/(.*)/g;
    const match = regex.exec(link);
    if (match) {
      return match[3];
    }
    else {
      return '';
    }
  }
}
