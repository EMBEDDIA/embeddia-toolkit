import {Component, OnDestroy, OnInit} from '@angular/core';
import {CoreService} from '../core/core.service';
import {HttpErrorResponse} from '@angular/common/http';
import {Disk, Memory} from '../shared/types/Health';
import {takeUntil} from 'rxjs/operators';
import {Subject} from 'rxjs';

@Component({
  selector: 'app-health',
  templateUrl: './health.component.html',
  styleUrls: ['./health.component.less']
})
export class HealthComponent implements OnInit, OnDestroy {

  disk = 0;
  cpu = 0;
  memory = 0;
  memoryObj: Memory;
  diskObj: Disk;
  services: { key: string, value: boolean }[];
  loading = true;
  destroyed$: Subject<boolean> = new Subject<boolean>();

  constructor(private coreService: CoreService) {
  }


  // router reuse strat? endpoint is slow
  ngOnInit(): void {
    this.coreService.getHealth().pipe(takeUntil(this.destroyed$)).subscribe(x => {
      if (x && !(x instanceof HttpErrorResponse)) {
        this.memoryObj = x.memory;
        this.diskObj = x.disk;
        this.cpu = x.cpu.percent;
        this.disk = Math.ceil(x.disk.used / x.disk.total * 100);
        this.memory = Math.ceil(x.memory.used / x.memory.total * 100);
        this.services = Object.keys(x.services).flatMap(y => [{key: y, value: x.services[y]}]);
      }
    }, () => null, () => this.loading = false);
  }
  ngOnDestroy(): void {
    this.destroyed$.next(true);
    this.destroyed$.complete();
  }
}
