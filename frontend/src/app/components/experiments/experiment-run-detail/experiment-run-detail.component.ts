import { FlatTreeControl } from '@angular/cdk/tree';
import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { MatTreeFlatDataSource, MatTreeFlattener } from '@angular/material/tree';
import { Observable, Subscription, catchError, interval, mergeMap, of, retry, switchMap, tap } from 'rxjs';
import { ExperimentRunDetails } from 'src/app/models/experiment-run';
import { BackendApiService } from 'src/app/services/backend-api.service';
import { SnackBarService } from 'src/app/services/snack-bar.service';

interface FoodNode {
  name: string;
  children?: FoodNode[];
}

interface ExampleFlatNode {
  originalNode: FoodNode;
  expandable: boolean;
  name: string;
  level: number;
}

const TREE_DATA: FoodNode[] = [
  {
    name: 'Fruit',
    children: [{ name: 'Apple' }, { name: 'Banana' }, { name: 'Fruit loops' }],
  },
  {
    name: 'Vegetables',
    children: [
      {
        name: 'Green',
        children: [{ name: 'Broccoli' }, { name: 'Brussels sprouts' }],
      },
      {
        name: 'Orange',
        children: [{ name: 'Pumpkins' }, { name: 'Carrots' }],
      },
    ],
  },
];



@Component({
  selector: 'app-experiment-run-detail',
  templateUrl: './experiment-run-detail.component.html',
  styleUrls: ['./experiment-run-detail.component.scss']
})
export class ExperimentRunDetailComponent {
  @Input()
  set runId(id: string) {
    this.subscription = this.backend.getExperimentRun(id).pipe(
      switchMap(run => {
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

        let logs = JSON.parse(this.experimentRun.logs)["job_logs"];
        let key = Object.keys(logs)[0];
        this.logs = logs[key]["logs"];

        if (run.state != 'CREATED' && run.state != 'IN_PROGRESS') {
          this.subscription.unsubscribe();
        }
      },
      error: err => {
        this.snackBar.showError(`Couldn't load experiment run: ${err.message}`);
      }
    });
  }

  /////////////////////////////////////

  private _transformer = (node: FoodNode, level: number) => {
    return {
      originalNode: node,
      expandable: !!node.children && node.children.length > 0,
      name: node.name,
      level: level,
    };
  };

  treeControl = new FlatTreeControl<ExampleFlatNode>(
    node => node.level,
    node => node.expandable,
  );

  treeFlattener = new MatTreeFlattener(
    this._transformer,
    node => node.level,
    node => node.expandable,
    node => node.children,
  );

  dataSource = new MatTreeFlatDataSource(this.treeControl, this.treeFlattener);

  hasChild = (_: number, node: ExampleFlatNode) => node.expandable;

  printout(val: String): void {
    console.log(val);
  }

  /////////////////////////////////////


  ngOnDestroy() {
    this.subscription?.unsubscribe();
  }

  logs: string = "";

  experimentRun: ExperimentRunDetails;
  subscription: Subscription;

  constructor(
    private backend: BackendApiService,
    private snackBar: SnackBarService
  ) { 
    this.dataSource.data = TREE_DATA;
  }

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
