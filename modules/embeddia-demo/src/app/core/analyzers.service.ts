import { Injectable } from '@angular/core';
import {LogService} from './log.service';
import {HttpClient, HttpErrorResponse} from '@angular/common/http';
import {environment} from '../../environments/environment';
import {Observable} from 'rxjs';
import {catchError, tap} from 'rxjs/operators';
import {AnalyzersOptions} from '../shared/types/AnalyzersOptions';
import {HateSpeechResponse} from '../shared/types/HateSpeechResponse';
import {KeywordExtractionResponse} from '../shared/types/KeywordExtractionResponse';

@Injectable({
  providedIn: 'root'
})
export class AnalyzersService {

  apiUrl = environment.apiHost + environment.apiBasePath;

  constructor(private http: HttpClient, private logService: LogService) {}

  getAnalyzersOptions(): Observable<AnalyzersOptions | HttpErrorResponse> {
    return this.http.options<AnalyzersOptions>(
      `${this.apiUrl}/article_analyzer/`
    ).pipe(
      tap(e => this.logService.logStatus(e, 'getAnalyzersOptions')),
      catchError(this.logService.handleError<AnalyzersOptions>('getAnalyzersOptions')));
  }

  analyzeHateSpeech(body: any): Observable<HateSpeechResponse | HttpErrorResponse> {
    return this.http.post<HateSpeechResponse>(
      `${this.apiUrl}/comment_analyzer/`, body
    ).pipe(
      tap(e => this.logService.logStatus(e, 'analyzeHateSpeech')),
      catchError(this.logService.handleError<HateSpeechResponse>('analyzeHateSpeech')));
  }

  analyzeKeywords(body: any): Observable<KeywordExtractionResponse | HttpErrorResponse> {
    return this.http.post<KeywordExtractionResponse>(
      `${this.apiUrl}/article_analyzer/`, body
    ).pipe(
      tap(e => this.logService.logStatus(e, 'analyzeKeywords')),
      catchError(this.logService.handleError<KeywordExtractionResponse>('analyzeKeywords')));
  }

}
