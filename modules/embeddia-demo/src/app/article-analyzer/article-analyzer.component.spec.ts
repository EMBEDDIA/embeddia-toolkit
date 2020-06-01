import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ArticleAnalyzerComponent } from './article-analyzer.component';

describe('ArticleAnalyzerComponent', () => {
  let component: ArticleAnalyzerComponent;
  let fixture: ComponentFixture<ArticleAnalyzerComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ArticleAnalyzerComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ArticleAnalyzerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
