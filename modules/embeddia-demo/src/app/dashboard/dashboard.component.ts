import {ChangeDetectionStrategy, ChangeDetectorRef, Component, HostListener, OnInit} from '@angular/core';
import {UtilityFunctions} from '../shared/UtilityFunctions';

interface GraphData {
  name: string;
  value: number;
  extra: { date: Date };
}

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.less'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class DashboardComponent implements OnInit {
  readonly COLORS = UtilityFunctions.COLORS;
  strokeCap: 'round' | 'square' = 'square';
  strokeWidth = 9; // %
  blockedByModelProgressWidth = 0;
  commentsOkProgressWidth = 0;
  tags: { PER: GraphData[], LOC: GraphData[], KEYWORD: GraphData[] } = {
    PER: [],
    LOC: [],
    KEYWORD: []
  };
  tagsKeys = Object.keys(this.tags);

  // options
  showXAxis = true;
  showYAxis = true;
  showXAxisLabel = true;
  xAxisLabel = 'Count';
  showYAxisLabel = true;
  yAxisLabel = 'Entities & Keywords';
  selectedFact;
  graphData: GraphData[] = [];


  isLoading = false;
  selectedDataset: string;
  selectedRange;
  dataset = [{value: 'test', display_name: 'test2'}];
  customColors: { name: string, value: string }[] = [];

  constructor(private changeDetectorRef: ChangeDetectorRef) {
  }

  @HostListener('window:resize')
  onResize() {
    this.calculateProgressBarSize();
  }

  ngOnInit(): void {
    for (let f = 0; f <= 10; f++) {
      const perName = Math.random().toString(36).substring(Math.random() * 10);
      this.tags.PER.push({
        name: perName, value: Math.floor(Math.random() * 100), extra: {date: this.randomDate(new Date(2012, 0, 1), new Date())}
      });
      this.customColors.push({name: perName, value: this.COLORS.PER});
      const keyName = Math.random().toString(36).substring(Math.random() * 10);
      this.tags.KEYWORD.push({
        name: keyName, value: Math.floor(Math.random() * 100), extra: {date: this.randomDate(new Date(2012, 0, 1), new Date())}
      });
      this.customColors.push({name: keyName, value: this.COLORS.KEYWORD});
      const locName = Math.random().toString(36).substring(Math.random() * 10);
      this.tags.LOC.push({
        name: locName,
        value: Math.floor(Math.random() * 100), extra: {date: this.randomDate(new Date(2012, 0, 1), new Date())}
      });
      this.customColors.push({name: locName, value: this.COLORS.LOC});
    }
    this.selectedDataset = this.dataset[0].value;
    this.selectedRange = [new Date(2012, 0, 1), new Date()];
    this.calculateProgressBarSize();

  }

  calculateProgressBarSize() {
    const windowHeight = window.innerHeight;
    if (windowHeight <= 790) {
      this.blockedByModelProgressWidth = 88;
      this.commentsOkProgressWidth = 108;
    } else if (windowHeight <= 876) {
      this.blockedByModelProgressWidth = 100;
      this.commentsOkProgressWidth = 115;
    } else if (windowHeight <= 960) {
      this.blockedByModelProgressWidth = 128;
      this.commentsOkProgressWidth = 148;
    } else {
      this.blockedByModelProgressWidth = 148;
      this.commentsOkProgressWidth = 168;
    }
  }

  getSelectedFacts(facts, dateRange: [Date, Date], data): GraphData[] {
    console.log(facts);
    console.log(data);
    const temp: GraphData[] = [];
    for (const key of facts) {
      if (data[key]) {
        temp.push(...data[key].filter(y => y.extra.date.getTime() >= dateRange[0].getTime() && y.extra.date.getTime() <= dateRange[1].getTime()));
      }
    }
    temp.sort((a, b) => (a.value < b.value) ? 1 : -1);
    return temp;
  }

  factSelectionChanged(val) {
    this.graphData = this.getSelectedFacts(val, this.selectedRange, this.tags);
  }

  submitForm() {
    this.isLoading = true;
    this.selectedFact = ['PER', 'LOC', 'KEYWORD'];
    this.graphData = this.getSelectedFacts(this.selectedFact, this.selectedRange, this.tags);
    this.isLoading = false;
  }

  formatYAxisTicks(val) {
    const split = val.split(' ');
    let stringValue = '';
    for (const item of split) {
      if (stringValue.length + item.length < 16) {
        stringValue += item + (split.length !== 1 ? ' ' : '');
      } else if (stringValue === '') {
        return split[0].substr(0, 16) + (split.length > 1 ? '...' : '');
      }
    }
    return val.length === stringValue.trim().length ? stringValue : stringValue + '...';
  }

  randomDate(start, end) {
    return new Date(start.getTime() + Math.random() * (end.getTime() - start.getTime()));
  }

}
