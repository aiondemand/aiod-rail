import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, catchError, combineLatest, of, switchMap, tap, throwError } from 'rxjs';
import { Dataset } from '../models/dataset';
import { environment } from 'src/environments/environment';
import { Platform } from '../models/platform';
import { ExperimentCreate, Experiment } from '../models/experiment';
import { Model } from '../models/model';
import { ExperimentTemplateCreate, ExperimentTemplate } from '../models/experiment-template';
import { Publication } from '../models/publication';
import { ExperimentRun, ExperimentRunDetails } from '../models/experiment-run';


@Injectable({
  providedIn: 'root'
})
export class BackendApiService {

  mockedSavedDatasets: Dataset[] = [];

  constructor(private http: HttpClient) {
    const savedDatasets = localStorage.getItem('savedDatasets');
    if (savedDatasets) {
      this.mockedSavedDatasets = JSON.parse(savedDatasets);
    }
  }

  ////////////////////////////// DATASETS //////////////////////////////

  getDatasets(query: string = "", offset: number = 0, limit: number = environment.DEFAULT_PAGE_SIZE): Observable<Dataset[]> {
    // TODO: handle the "is_in_my_saved" property on backend

    var backend_route = `${environment.BACKEND_API_URL}/assets/datasets`;
    if (query?.length > 0) {
      backend_route += `/search/${query}`
    }
    backend_route += `?offset=${offset}&limit=${limit}`

    return this.http.get<Dataset[]>(backend_route)
      .pipe(tap(datasets => {
        datasets.forEach(dataset => {
          dataset.is_in_my_saved = this.mockedSavedDatasets.some(d => d.identifier === dataset.identifier);
        });
      }));
  }

  getDatasetsCount(query: string = ""): Observable<number> {
    var backend_route = `${environment.BACKEND_API_URL}/assets/counts/datasets`;
    if (query?.length > 0) {
      backend_route += `/search/${query}`
    }

    return this.http.get<number>(backend_route);
  }

  getDataset(id: string): Observable<Dataset> {
    // TODO: handle the "is_in_my_saved" property on backend
    return this.http.get<Dataset>(`${environment.BACKEND_API_URL}/assets/datasets/${id}`)
      .pipe(tap(dataset => {
        dataset.is_in_my_saved = this.mockedSavedDatasets.some(d => d.identifier === dataset.identifier);
      }));
  }

  createDataset(dataset: Dataset, file: any, hf_username: string = '', hf_token: string = ''): Observable<Dataset> {
    if (dataset.platform === 'huggingface') {
      return this.http.post<Dataset>(`${environment.BACKEND_API_URL}/assets/datasets`, dataset)
        .pipe(
          switchMap(dataset => this.uploadDatasetToHuggingFace(dataset, file, hf_username, hf_token))
        );
    }
    return this.http.post<Dataset>(`${environment.BACKEND_API_URL}/assets/datasets`, dataset);
  }

  /**
   * Try to upload the dataset to HuggingFace. If the upload fails, delete the dataset from the backend
   * and throw the original error.
   * @param dataset
   * @param file
   * @param hf_username
   * @param hf_token
   * @returns
   */
  private uploadDatasetToHuggingFace(dataset: Dataset, file: any, hf_username: string, hf_token: string): Observable<Dataset> {
    const formData = new FormData();
    formData.append('file', file, file.name);

    return this.http.post<Dataset>(
      `${environment.BACKEND_API_URL}/assets/datasets/${dataset.identifier}/upload-file-to-huggingface`
      + `?huggingface_name=${hf_username}&huggingface_token=${hf_token}`,
      formData
    ).pipe(
      catchError(err => {
        return this.deleteDataset(dataset).pipe(
          switchMap(_ => throwError(() => new Error(err)))
        )
      })
    );
  }

  private deleteDataset(dataset: Dataset): Observable<boolean> {
    return this.http.delete<Dataset>(`${environment.BACKEND_API_URL}/assets/datasets/${dataset.identifier}`)
      .pipe(
        switchMap(_ => {
          return this.removeFromSaved(dataset);
        }),
        catchError(err => throwError(() => new Error(err)))
      );
  }

  saveDataset(dataset: Dataset): Observable<boolean> {
    // TODO: call the backend API to save the dataset once we have the endpoint
    this.mockedSavedDatasets.push(dataset);
    localStorage.setItem('savedDatasets', JSON.stringify(this.mockedSavedDatasets));
    return of(true);
  }

  removeFromSaved(dataset: Dataset): Observable<boolean> {
    this.mockedSavedDatasets = this.mockedSavedDatasets.filter(d => d.identifier !== dataset.identifier);
    localStorage.setItem('savedDatasets', JSON.stringify(this.mockedSavedDatasets));
    return of(true);
  }

  getSavedDatasets(offset: number = 0, limit: number = environment.DEFAULT_PAGE_SIZE): Observable<Dataset[]> {
    // TODO: call the backend API to get the saved datasets once we have the endpoint
    // TODO: handle the "is_in_my_saved" property on backend
    return of(this.mockedSavedDatasets.slice(offset, offset + limit))
      .pipe(tap(datasets => {
        datasets.forEach(dataset => dataset.is_in_my_saved = true);
      }));
  }

  getSavedDatasetsCount(): Observable<number> {
    // TODO: call the backend API to get the saved datasets count once we have the endpoint
    return of<number>(this.mockedSavedDatasets.length);
  }

  ////////////////////////////// MODELS //////////////////////////////

  /**
   * Get list of models
   * @returns Observable<Model[]>
   * @param query
   * @param offset
   * @param limit
   */
  getModels(query: string = "", offset: number = 0, limit: number = environment.DEFAULT_PAGE_SIZE): Observable<Model[]> {
    var backend_route = `${environment.BACKEND_API_URL}/assets/models`;
    if (query?.length > 0) {
      backend_route += `/search/${query}`
    }
    backend_route += `?offset=${offset}&limit=${limit}`

    return this.http.get<Model[]>(backend_route);
  }

  /**
   * Get model by id
   * @returns Observable<Model>
   */
  getModel(id: string): Observable<Model> {
    return this.http.get<Model>(`${environment.BACKEND_API_URL}/assets/models/${id}`);
  }

  getModelsCount(query: string = ""): Observable<number> {
    var backend_route = `${environment.BACKEND_API_URL}/assets/counts/models`;
    if (query?.length > 0) {
      backend_route += `/search/${query}`
    }
    
    return this.http.get<number>(backend_route);
  }

  ////////////////////////////// PUBLICATIONS //////////////////////////////

  /**
   * Get experiment related publications
   * @returns Observable<Publication[]>
   * @param experiment
   */
  getExperimentPublications(experiment: Experiment): Observable<Publication[]> {
    if (!experiment.publication_ids || experiment.publication_ids.length === 0) {
      return of([]);
    }
    return combineLatest(experiment.publication_ids.map(id => this.getPublication(id)));
  }

   /**
   * Get list of publications
   * @returns Observable<Publication[]>
   * @param query
   * @param offset
   * @param limit
   */
   getPublications(query: string = "", offset: number = 0, limit: number = environment.DEFAULT_PAGE_SIZE): Observable<Publication[]> {
    var backend_route = `${environment.BACKEND_API_URL}/assets/publications`;
    if (query?.length > 0) {
      backend_route += `/search/${query}`
    }
    backend_route += `?offset=${offset}&limit=${limit}`

    return this.http.get<Publication[]>(backend_route);
  }

  /**
   * Get list of publications
   * @returns Observable<Publication>
   * @param publicationId
   */
  getPublication(publicationId: string): Observable<Publication> {
    return this.http.get<Publication>(`${environment.BACKEND_API_URL}/assets/publications/${publicationId}`);
  }

  getPublicationsCount(query: string = ""): Observable<number> {
    var backend_route = `${environment.BACKEND_API_URL}/assets/counts/publications`;
    if (query?.length > 0) {
      backend_route += `/search/${query}`
    }

    return this.http.get<number>(backend_route);
  }

  ////////////////////////////// MISC //////////////////////////////

  /**
   * Tests an API that requires authentication on backend.
   * Fails if the user is not authenticated.
   * @returns Observable<any>
   */
  authenticationTest(): Observable<any> {
    return this.http.get<any>(`${environment.BACKEND_API_URL}/assets/authentication_test`);
  }

  /**
   * Get list of platforms from the backend.
   * @returns Observable<Platform[]>
   */
  getPlatforms(): Observable<Platform[]> {
    return this.http.get<Platform[]>(`${environment.BACKEND_API_URL}/assets/platforms`);
  }

  ////////////////////////////// EXPERIMENTS //////////////////////////////

  /**
   * Get list of experiments
   * @returns Observable<Experiment[]>
   */
  getExperiments(offset: number = 0, limit: number = environment.DEFAULT_PAGE_SIZE): Observable<Experiment[]> {
    return this.http.get<Experiment[]>(`${environment.BACKEND_API_URL}/experiments`);
  }

  /**
 * Get list of user experiments
 * @returns Observable<Experiment[]>
 */
  getMyExperiments(offset: number = 0, limit: number = environment.DEFAULT_PAGE_SIZE): Observable<Experiment[]> {
    return this.http.get<Experiment[]>(`${environment.BACKEND_API_URL}/experiments/my`);
  }

  /**
   * Get an experiment by id
   * @returns Observable<ExperimentObservable>
   * @param id
   */
  getExperiment(id: string): Observable<Experiment> {
    return this.http.get<Experiment>(`${environment.BACKEND_API_URL}/experiments/${id}`);
  }

  /**
   * Get count of experiments
   * @returns Observable<number> (count)
   */
  getExperimentsCount(): Observable<number> {
    return this.http.get<number>(`${environment.BACKEND_API_URL}/count/experiments`);
  }

  /**
  * Get count of experiments
  * @returns Observable<number> (count)
  */
  getMyExperimentsCount(): Observable<number> {
    return this.http.get<number>(`${environment.BACKEND_API_URL}/count/experiments/my`);
  }

  /**
   * Create experiment
   * @returns Observable<Experiment>
   * @param experiment
   */
  createExperiment(experiment: ExperimentCreate): Observable<Experiment> {
    return this.http.post<Experiment>(`${environment.BACKEND_API_URL}/experiments`, experiment);
  }

  ////////////////////////////// EXPERIMENT TEMPLATES //////////////////////////////

  /**
   * Get list of experiment templates
   * @returns Observable<ExperimentTemplate[]>
   */
  getExperimentTemplates(offset: number = 0, limit: number = environment.DEFAULT_PAGE_SIZE): Observable<ExperimentTemplate[]> {
    return this.http.get<ExperimentTemplate[]>(`${environment.BACKEND_API_URL}/experiment-templates`
      + `?offset=${offset}&limit=${limit}`);
  }

  getApprovedExperimentTemplates(offset: number = 0, limit: number = environment.DEFAULT_PAGE_SIZE): Observable<ExperimentTemplate[]> {
    return this.http.get<ExperimentTemplate[]>(`${environment.BACKEND_API_URL}/experiment-templates/approved`
      + `?offset=${offset}&limit=${limit}`);
  }

  getMyExperimentTemplates(offset: number = 0, limit: number = environment.DEFAULT_PAGE_SIZE): Observable<ExperimentTemplate[]> {
    return this.http.get<ExperimentTemplate[]>(`${environment.BACKEND_API_URL}/experiment-templates/my`
      + `?offset=${offset}&limit=${limit}`);
  }

  getExperimentTemplatesAllView(offset: number = 0, limit: number = environment.DEFAULT_PAGE_SIZE): Observable<ExperimentTemplate[]> {
    return this.http.get<ExperimentTemplate[]>(`${environment.BACKEND_API_URL}/experiment-templates/all-view`
      + `?offset=${offset}&limit=${limit}`);
  }

  /**
   * Get experiment template by id
   * @returns Observable<ExperimentTemplate>
   * @param id
   */
  getExperimentTemplate(id: string): Observable<ExperimentTemplate> {
    return this.http.get<ExperimentTemplate>(`${environment.BACKEND_API_URL}/experiment-templates/${id}`);
  }

  /**
   * Get count of experiment templates
   * @returns Observable<number> (count)
   */
  getExperimentTemplatesCount(): Observable<number> {
    return this.http.get<number>(`${environment.BACKEND_API_URL}/count/experiment-templates`);
  }

  getApprovedExperimentTemplatesCount(): Observable<number> {
    return this.http.get<number>(`${environment.BACKEND_API_URL}/count/experiment-templates`);
  }

  getMyExperimentTemplatesCount(): Observable<number> {
    return this.http.get<number>(`${environment.BACKEND_API_URL}/count/experiment-templates/my`);
  }

  getExperimentTemplatesAllViewCount(): Observable<number> {
    return this.http.get<number>(`${environment.BACKEND_API_URL}/count/experiment-templates/all-view`);
  }

  /**
   * Create new experiment template
   * @returns Observable<ExperimentTemplate> (count)
   */
  createExperimentTemplate(experimentTemplate: ExperimentTemplateCreate): Observable<ExperimentTemplate> {
    return this.http.post<ExperimentTemplate>(`${environment.BACKEND_API_URL}/experiment-templates`, experimentTemplate);
  }

  ////////////////////////////// EXPERIMENT RUNS //////////////////////////////

  /**
   * Get list of experiment runs
   * @returns Observable<ExperimentRun[]>
   * @param offset
   * @param limit
   * @param experimentId
   */
  getExperimentRuns(experimentId: string = "", offset: number = 0, limit: number = environment.DEFAULT_PAGE_SIZE): Observable<ExperimentRun[]> {
    if (experimentId == "") {
      return this.http.get<ExperimentRun[]>(`${environment.BACKEND_API_URL}/experiment-runs?offset=${offset}&limit=${limit}`);
    }    
    return this.http.get<ExperimentRun[]>(`${environment.BACKEND_API_URL}/experiments/${experimentId}/runs?offset=${offset}&limit=${limit}`);
  }

  getExperimentRunsCount(experimentId: string): Observable<number> {
    return this.http.get<number>(`${environment.BACKEND_API_URL}/count/experiments/${experimentId}/runs`);
  }
  
  /**
   * Get experiment run by id
   * @returns Observable<ExperimentRun>
   * @param experimentRunId
   */
  getExperimentRun(experimentRunId: string): Observable<ExperimentRunDetails> {
    return this.http.get<ExperimentRunDetails>(`${environment.BACKEND_API_URL}/experiment-runs/${experimentRunId}`);
  }

  /**
   * Get logs for experiment run
   * @returns Observable<string>
   * @param experimentRunId
   */
  getExperimentRunLogs(experimentRunId: string): Observable<string> {
    return this.http.get<string>(`${environment.BACKEND_API_URL}/experiment-runs/${experimentRunId}/logs`,
      { responseType: 'text' as 'json' });
  }

  /**
   * Execute (Create) experiment run
   * @returns Observable<ExperimentRun>
   * @param experimentId
   */
  executeExperimentRun(experimentId: string): Observable<ExperimentRun> {
    return this.http.get<ExperimentRun>(`${environment.BACKEND_API_URL}/experiments/${experimentId}/execute`);
  }
}
