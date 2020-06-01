import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ArticleGenerationComponent } from './article-generation.component';

describe('ArticleGenerationComponent', () => {
  let component: ArticleGenerationComponent;
  let fixture: ComponentFixture<ArticleGenerationComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ArticleGenerationComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ArticleGenerationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
