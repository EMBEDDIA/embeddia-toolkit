import {Injectable} from '@angular/core';
import {environment} from '../../environments/environment';
import {Observable, of} from 'rxjs';
import {HttpErrorResponse} from '@angular/common/http';
import {NzMessageService} from 'ng-zorro-antd';


@Injectable({
  providedIn: 'root'
})
export class LogService {
  isProduction = environment.production;

  constructor(private message: NzMessageService) {
  }

  public handleError<T>(operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {
      // TODO: send the error to remote logging infrastructure
      console.warn(error); // log to console instead

      return of(error);
    };
  }


  public logStatus(val, msg) {
    if (!this.isProduction) {
      console.warn(msg, val);
    }
  }

  public messageHttpError(error: HttpErrorResponse, time?: number) {
    this.message.create('error', `${error.name}: ${error.status} ${error.statusText}`,
      {
        nzDuration: time || 3000
      });
  }

  public createMessage(type: 'success' | 'info' | 'warning' | 'error' | 'loading', msg: string, time?: number) {
    this.message.create(type, msg, {
      nzDuration: time || 3000
    });
  }
}
