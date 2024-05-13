import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { catchError, combineLatest, Observable, of, switchMap, tap, throwError } from 'rxjs';
import { Dataset } from '../models/dataset';
import { environment } from 'src/environments/environment';
import { Platform } from '../models/platform';
import { Experiment, ExperimentCreate } from '../models/experiment';
import { Model } from '../models/model';
import { ExperimentTemplate, ExperimentTemplateCreate } from '../models/experiment-template';
import { Publication } from '../models/publication';
import { ExperimentRun, ExperimentRunDetails } from '../models/experiment-run';
import { ExperimentQueries, ExperimentTemplateQueries, PageQueries } from '../models/queries';
import { FileDetail } from '../models/file-detail';


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

  getDatasets(query: string = "", pageQueries?: PageQueries): Observable<Dataset[]> {
    // TODO: handle the "is_in_my_saved" property on backend
    let backend_route = `${environment.BACKEND_API_URL}/assets/datasets`;
    if (query?.length > 0) {
      backend_route += `/search/${query}`
    }
    backend_route += `?${this._buildPageQueries(pageQueries)}`;

    return this.http.get<Dataset[]>(backend_route)
      .pipe(tap(datasets => {
        datasets.forEach(dataset => {
          dataset.is_in_my_saved = this.mockedSavedDatasets.some(d => d.identifier === dataset.identifier);
        });
      }));
  }

  getDatasetsCount(query: string = ""): Observable<number> {
    let backend_route = `${environment.BACKEND_API_URL}/assets/counts/datasets`;
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

  getSavedDatasets(pageQueries?: PageQueries): Observable<Dataset[]> {
    // TODO: call the backend API to get the saved datasets once we have the endpoint
    // TODO: handle the "is_in_my_saved" property on backend
    let offset = pageQueries?.offset ?? 0;
    let limit = pageQueries?.limit ?? environment.DEFAULT_PAGE_SIZE;

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
   * @param pageQueries
   */
  getModels(query: string = "", pageQueries?: PageQueries): Observable<Model[]> {
    let backend_route = `${environment.BACKEND_API_URL}/assets/models`;
    if (query?.length > 0) {
      backend_route += `/search/${query}`
    }
    backend_route += `?${this._buildPageQueries(pageQueries)}`;

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
    let backend_route = `${environment.BACKEND_API_URL}/assets/counts/models`;
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
   * @param pageQueries
   */
  getPublications(query: string = "", pageQueries?: PageQueries): Observable<Publication[]> {
    let backend_route = `${environment.BACKEND_API_URL}/assets/publications`;
    if (query?.length > 0) {
      backend_route += `/search/${query}`
    }
    backend_route += `?${this._buildPageQueries(pageQueries)}`;

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
    let backend_route = `${environment.BACKEND_API_URL}/assets/counts/publications`;
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
  getExperiments(
    query: string,
    pageQueries?: PageQueries,
    experimentQueries?: ExperimentQueries
  ): Observable<Experiment[]> {
    let queries = `?query=${query}&${this._buildPageQueries(pageQueries)}&${this._buildExperimentQueries(experimentQueries)}`;
    return this.http.get<Experiment[]>(`${environment.BACKEND_API_URL}/experiments${queries}`);
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
  getExperimentsCount(query: string, experimentQueries?: ExperimentQueries): Observable<number> {
    let queries = `?$query=${query}&${this._buildExperimentQueries(experimentQueries)}`;
    return this.http.get<number>(`${environment.BACKEND_API_URL}/count/experiments${queries}`);
  }

  isExperimentMine(id: string): Observable<boolean> {
    return this.http.get<boolean>(`${environment.BACKEND_API_URL}/experiments/${id}/is_mine`);
  }

  /**
   * Create experiment
   * @returns Observable<Experiment>
   * @param experiment
   */
  createExperiment(experiment: ExperimentCreate): Observable<Experiment> {
    return this.http.post<Experiment>(`${environment.BACKEND_API_URL}/experiments`, experiment);
  }

  updateExperiment(id: string, experiment: ExperimentCreate): Observable<Experiment> {
    return this.http.put<Experiment>(`${environment.BACKEND_API_URL}/experiments/${id}`, experiment);
  }

  setExperimentUsability(id: string, is_usable: boolean): Observable<void> {
    return this.http.patch<void>(`${environment.BACKEND_API_URL}/experiments/${id}/usability?is_usable=${is_usable}`, {});
  }

  deleteExperiment(id: string): Observable<boolean> {
    return this.http.delete<boolean>(`${environment.BACKEND_API_URL}/experiments/${id}`);
  }

  ////////////////////////////// EXPERIMENT TEMPLATES //////////////////////////////

  /**
   * Get list of experiment templates
   * @returns Observable<ExperimentTemplate[]>
   */
  getExperimentTemplates(
    query: string,
    pageQueries?: PageQueries,
    templateQueries?: ExperimentTemplateQueries
  ): Observable<ExperimentTemplate[]> {
    let queries = `?query=${query}&${this._buildPageQueries(pageQueries)}&${this._buildExperimentTemplateQueries(templateQueries)}`;
    return this.http.get<ExperimentTemplate[]>(`${environment.BACKEND_API_URL}/experiment-templates${queries}`);
  }

  /**
   * Get experiment template by id
   * @returns Observable<ExperimentTemplate>
   * @param id
   */
  getExperimentTemplate(id: string): Observable<ExperimentTemplate> {
    return this.http.get<ExperimentTemplate>(`${environment.BACKEND_API_URL}/experiment-templates/${id}`);
  }

  isExperimentTemplateMine(id: string): Observable<boolean> {
    return this.http.get<boolean>(`${environment.BACKEND_API_URL}/experiment-templates/${id}/is_mine`);
  }

  /**
   * Get count of experiment templates
   * @returns Observable<number> (count)
   */
  getExperimentTemplatesCount(
    query: string,
    templateQueries?: ExperimentTemplateQueries
  ): Observable<number> {
    let queries = `?query=${query}&${this._buildExperimentTemplateQueries(templateQueries)}`;
    return this.http.get<number>(`${environment.BACKEND_API_URL}/count/experiment-templates${queries}`);
  }

  getExperimentsOfTemplateCount(id: string): Observable<number> {
    return this.http.get<number>(`${environment.BACKEND_API_URL}/count/experiment-templates/${id}/experiments`);
  }

  /**
   * Create new experiment template
   * @returns Observable<ExperimentTemplate> (count)
   */
  createExperimentTemplate(experimentTemplate: ExperimentTemplateCreate): Observable<ExperimentTemplate> {
    return this.http.post<ExperimentTemplate>(`${environment.BACKEND_API_URL}/experiment-templates`, experimentTemplate);
  }

  updateExperimentTemplate(id: string, experimentTemplate: ExperimentTemplateCreate): Observable<ExperimentTemplate> {
    return this.http.put<ExperimentTemplate>(`${environment.BACKEND_API_URL}/experiment-templates/${id}`, experimentTemplate);
  }

  setExperimentTemplateUsability(id: string, is_usable: boolean): Observable<void> {
    return this.http.patch<void>(`${environment.BACKEND_API_URL}/experiment-templates/${id}/usability?is_usable=${is_usable}`, {});
  }

  deleteExperimentTemplate(id: string): Observable<void> {
    return this.http.delete<void>(`${environment.BACKEND_API_URL}/experiment-templates/${id}`);
  }

  ////////////////////////////// EXPERIMENT RUNS //////////////////////////////

  /**
   * Get list of experiment runs
   * @returns Observable<ExperimentRun[]>
   * @param pageQueries
   * @param experimentId
   */
  getExperimentRuns(experimentId: string = "", pageQueries?: PageQueries): Observable<ExperimentRun[]> {
    let pageQueriesStr = `?${this._buildPageQueries(pageQueries)}`;

    if (experimentId == "") {
      return this.http.get<ExperimentRun[]>(`${environment.BACKEND_API_URL}/experiment-runs${pageQueriesStr}`);
    }
    return this.http.get<ExperimentRun[]>(`${environment.BACKEND_API_URL}/experiments/${experimentId}/runs${pageQueriesStr}`);
  }

  getExperimentRunsCount(experimentId: string): Observable<number> {
    return this.http.get<number>(`${environment.BACKEND_API_URL}/count/experiments/${experimentId}/runs`);
  }


  listFilesFromExperimentRun(experimentId: string): Observable<FileDetail[]> {
    return this.http.get<FileDetail[]>(`${environment.BACKEND_API_URL}/experiment-runs/${experimentId}/files/list`);
  }

  downloadFileFromExperimentRun(experimentId: string, filepath: string): Observable<any> {
    return this.http.get(
      `${environment.BACKEND_API_URL}/experiment-runs/${experimentId}/files/download?filepath=${filepath}`,
      { responseType: 'blob', observe: 'response', reportProgress: true }
    );
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

  _buildPageQueries(pageQueries?: PageQueries): string {
    if (pageQueries == undefined) {
      pageQueries = {};
    }
    if (pageQueries.limit == null) {
      pageQueries.limit = environment.DEFAULT_PAGE_SIZE;
    }
    if (pageQueries.offset == null) {
      pageQueries.offset = 0;
    }
    return `offset=${pageQueries.offset}&limit=${pageQueries.limit}`
  }

  _buildExperimentQueries(experimentQueries?: ExperimentQueries): string {
    // TODO: Add query parameters
    return "";
  }

  _buildExperimentTemplateQueries(templateQueries?: ExperimentTemplateQueries): string {
    if (templateQueries == undefined) {
      return "";
    }

    let q: string = "";
    let key: keyof ExperimentTemplateQueries
    for (key in templateQueries) {
      q += `${key}=${templateQueries[key]}&`;
    }
    return q.slice(0, q.length - 1);
  }
}
