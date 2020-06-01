import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CommentAnalyzerComponent } from './comment-analyzer.component';

describe('CommentAnalyzerComponent', () => {
  let component: CommentAnalyzerComponent;
  let fixture: ComponentFixture<CommentAnalyzerComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CommentAnalyzerComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CommentAnalyzerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
