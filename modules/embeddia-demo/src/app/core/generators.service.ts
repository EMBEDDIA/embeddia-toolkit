import {Injectable} from '@angular/core';
import {environment} from '../../environments/environment';
import {HttpClient, HttpErrorResponse} from '@angular/common/http';
import {LogService} from './log.service';
import {Observable} from 'rxjs';
import {catchError, tap} from 'rxjs/operators';
import {GeneratorOptions} from '../shared/types/GeneratorOptions';
import {GeneratorResponse} from '../shared/types/GeneratorResponse';

@Injectable({
  providedIn: 'root'
})
export class GeneratorsService {

  apiUrl = environment.apiHost + environment.apiBasePath;

  constructor(private http: HttpClient, private logService: LogService) {
  }

  getGeneratorsOptions(): Observable<GeneratorOptions | HttpErrorResponse> {
    return this.http.options<GeneratorOptions>(
      `${this.apiUrl}/article_generator/`
    ).pipe(
      tap(e => this.logService.logStatus(e, 'getGeneratorsOptions')),
      catchError(this.logService.handleError<GeneratorOptions>('getGeneratorsOptions')));
  }

  generateText(body: any): Observable<GeneratorResponse | HttpErrorResponse> {
    return this.http.post<GeneratorResponse>(
      `${this.apiUrl}/article_generator/`, body
    ).pipe(
      tap(e => this.logService.logStatus(e, 'generateText')),
      catchError(this.logService.handleError<GeneratorResponse>('generateText')));
  }
}
