import {Component, OnDestroy, OnInit} from '@angular/core';
import {GeneratorsService} from '../core/generators.service';
import {HttpErrorResponse} from '@angular/common/http';
import {LogService} from '../core/log.service';
import {Choice} from '../shared/types/GeneratorOptions';
import {GeneratorResponse} from '../shared/types/GeneratorResponse';
import {Subject} from 'rxjs';
import {takeUntil} from 'rxjs/operators';

@Component({
  selector: 'app-article-generation',
  templateUrl: './article-generation.component.html',
  styleUrls: ['./article-generation.component.less']
})
export class ArticleGenerationComponent implements OnInit, OnDestroy {

  isLoading = false;
  dataset: Choice[] = [];
  location: Choice[] = [];
  language: Choice[] = [];
  selectedLocation: string;
  selectedDataset: string;
  selectedLanguage: string;
  results: GeneratorResponse | null;
  destroyed$: Subject<boolean> = new Subject<boolean>();

  constructor(private generatorsService: GeneratorsService, private logService: LogService) {
  }

  ngOnInit(): void {
    this.generatorsService.getGeneratorsOptions().pipe(takeUntil(this.destroyed$)).subscribe(x => {
      if (x && !(x instanceof HttpErrorResponse)) {
        this.dataset = x.actions.POST.dataset.choices;
        this.selectedDataset = this.dataset[0].value;
        this.location = x.actions.POST.location.choices;
        this.selectedLocation = this.location[0].value;
        this.language = x.actions.POST.language.choices;
        this.selectedLanguage = this.language[0].value;
      } else if (x instanceof HttpErrorResponse) {
        this.logService.messageHttpError(x);
      }
    });
  }

  submitForm() {
    this.isLoading = true;
    this.results = null;
    this.generatorsService.generateText(
      {location: this.selectedLocation, dataset: this.selectedDataset, language: this.selectedLanguage}).subscribe(x => {
      if (x && !(x instanceof HttpErrorResponse)) {
        this.results = x;
      } else if (x instanceof HttpErrorResponse) {
        this.logService.messageHttpError(x);
      }
    }, () => null, () => this.isLoading = false);
  }

  ngOnDestroy(): void {
    this.destroyed$.next(true);
    this.destroyed$.complete();
  }
}
