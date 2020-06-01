import { TestBed } from '@angular/core/testing';

import { AnalyzersService } from './analyzers.service';

describe('AnalyzersService', () => {
  let service: AnalyzersService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(AnalyzersService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
