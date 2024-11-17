import {AfterViewInit, ChangeDetectorRef, Component} from '@angular/core';
import {CommonModule} from '@angular/common';
import {FormsModule} from '@angular/forms';
import {DropdownModule} from 'primeng/dropdown';
import {CalendarModule} from 'primeng/calendar';
import {ButtonModule} from 'primeng/button';
import {InputTextModule} from 'primeng/inputtext';
import {TooltipModule} from 'primeng/tooltip';
import {InputTextareaModule} from 'primeng/inputtextarea';
import {MultiSelectModule} from 'primeng/multiselect';
import {AccordionModule} from "primeng/accordion";
import {TabMenuModule} from "primeng/tabmenu";
import * as am5 from '@amcharts/amcharts5';
import * as am5percent from '@amcharts/amcharts5/percent';
import * as am5xy from '@amcharts/amcharts5/xy';
import * as am5radar from '@amcharts/amcharts5/radar';
import * as am5hierarchy from '@amcharts/amcharts5/hierarchy';
import am5themes_Animated from '@amcharts/amcharts5/themes/Animated';

export interface ChildCategory {
  name: string;
  value: number;
  children?: ChildCategory[];
}

export interface Category {
  name: string;
  value: number;
  children: ChildCategory[];
}

export interface PercentageData {
  category: string;
  value: number;
}

export interface RadarData {
  category: string;
  value: number;
}

export interface CourtCase {
  id: number;
  similarity: number;
  trust: number;
  caseName: string;
  caseNumber: string;
  summary: string;
  verdict: string;
  date: string;
  categories: Category[];
  categoryPercentages: PercentageData[];
  radarData: RadarData[];
}

export type CourtCases = CourtCase[];

@Component({
  selector: 'app-file-search',
  standalone: true,
  templateUrl: './file-search.component.html',
  styleUrls: ['./file-search.component.scss', 'layout.css'],
  imports: [
    CommonModule,
    FormsModule,
    DropdownModule,
    CalendarModule,
    ButtonModule,
    InputTextModule,
    TooltipModule,
    InputTextareaModule,
    MultiSelectModule,
    AccordionModule,
    TabMenuModule,
  ]
})
export class FileSearchComponent implements AfterViewInit {
  searchQuery: string = '';
  searchCaseDetailsQuery: string = '';
  selectedLanguage: any;
  selectedCourt: any;
  startDate: Date | null = null;
  endDate: Date | null = null
  article: string = '';
  displayInfo: boolean = false;

  languages = [{name: 'English'}, {name: 'Greek'}, {name: 'French'}];
  courts = [{name: 'ECtHR'}, {name: 'CJEU'}, {name: 'CYLAW'}, {name: 'Cour de cassation'}];

  selectedChartType: { [key: number]: string } = {};
  chartOptions = [
    {label: 'Pie Chart', icon: 'pi pi-chart-pie'},
    {label: 'Radar Chart', icon: 'pi pi-compass'},
    {label: 'Force-Directed Tree', icon: 'pi pi-sitemap'},
  ];

  courtCases: CourtCases = [];

  onSearch() {
    console.log('Searching for:', this.searchQuery);

    const requestData = {
      query: this.searchQuery,
      searchCaseDetailsQuery: this.searchCaseDetailsQuery,
      language: this.selectedLanguage.name,
      selectedCourt: this.selectedCourt,
      startDate: this.startDate ? this.startDate.toISOString() : null,
      endDate: this.endDate ? this.endDate.toISOString() : null,
      article: this.article,
      displayInfo: this.displayInfo,
    };

    fetch('http://localhost:5001/search', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestData),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        console.log('Search results:', data);

        if (Array.isArray(data)) {
          this.courtCases = data;
          this.courtCases.sort((a, b) => b.similarity - a.similarity);
          this.cdr.detectChanges();
        } else {
          console.warn('Data received is not an array, converting to array format.');
          this.courtCases = Object.values(data);
        }

        this.initializeCharts();
      })
      .catch((error) => {
        console.error('Error during search:', error);
        alert('An error occurred while fetching the search results. Please try again.');
      });
  }

  clearAll() {
    console.log('Clearing search inputs and results...');
    this.searchQuery = '';
    this.searchCaseDetailsQuery = '';
    this.selectedLanguage = '';
    this.selectedCourt = '';
    this.startDate = null;
    this.endDate = null;
    this.article = '';
    this.displayInfo = false;
    this.courtCases = [];
  }

  constructor(private cdr: ChangeDetectorRef) {
  }

  ngAfterViewInit() {
    this.initializeCharts();
  }

  initializeCharts() {
    if (!this.courtCases || this.courtCases.length === 0) {
      console.warn('No court cases available for rendering charts.');
      return;
    }

    this.courtCases.forEach((courtCase: CourtCase) => {
      this.renderChart(courtCase.id, 'Pie Chart');
    });
  }

  onChartToggle(caseId: number, event: any) {
    const chartType = event.label;
    this.renderChart(caseId, chartType);
  }

  renderChart(caseId: number, chartType: string) {
    const chartContainer = `chart-container-${caseId}`;

    const existingRoot = am5.getRootById(chartContainer);
    if (existingRoot) {
      existingRoot.dispose();
    }

    const root = am5.Root.new(chartContainer);
    root.setThemes([am5themes_Animated.new(root)]);

    if (chartType === 'Pie Chart') {
      this.renderPieChart(root, this.getCaseDetails(caseId)!.categoryPercentages);
    } else if (chartType === 'Force-Directed Tree') {
      this.renderForceDirectedTree(root, caseId);
    } else if (chartType === 'Radar Chart') {
      this.renderRadarChart(root, this.getCaseDetails(caseId)!.radarData);
    }
  }

  getCaseDetails(caseId: number) {
    return this.courtCases.find((courtCase: any) => courtCase.id === caseId)!;
  }

  renderPieChart(root: am5.Root, data: any) {
    const chart = root.container.children.push(
      am5percent.PieChart.new(root, {
        layout: root.verticalLayout,
      })
    );

    const series = chart.series.push(
      am5percent.PieSeries.new(root, {
        valueField: 'value',
        categoryField: 'category',
      })
    );

    series.data.setAll(data);
  }

  renderForceDirectedTree(root: am5.Root, caseId: number) {
    const caseDetails = this.getCaseDetails(caseId);
    const categories = caseDetails ? caseDetails.categories : [];

    const data = {
      name: caseDetails?.caseName || 'Unknown Case',
      children: categories.map((category: any) => ({
        name: category.name,
        value: category.value,
        children: category.children?.map((subcategory: any) => ({
          name: subcategory.name,
          value: subcategory.value,
          children: subcategory.children?.map((subSubcategory: any) => ({
            name: subSubcategory.name,
            value: subSubcategory.value
          })) || []
        })) || []
      }))
    };
    console.log(data)
    var zoomableContainer = root.container.children.push(
      am5.ZoomableContainer.new(root, {
        width: am5.p100,
        height: am5.p100,
        wheelable: true,
        pinchZoom: true,
      })
    );

    var zoomTools = zoomableContainer.children.push(am5.ZoomTools.new(root, {
      target: zoomableContainer
    }));

    var series = zoomableContainer.contents.children.push(am5hierarchy.ForceDirected.new(root, {
        maskContent: false,
        singleBranchOnly: false,
        downDepth: 3,
        topDepth: 1,
        initialDepth: 2,
        valueField: 'value',
        categoryField: 'name',
        childDataField: 'children',
        idField: 'name',
        linkWithField: 'linkWith',
        manyBodyStrength: -50,
        centerStrength: 5,
        nodePadding: 1,
        minRadius: 20,
        maxRadius: am5.percent(15),
      })
    );

    series.get('colors')!.setAll({
      step: 2,
    });
    series.links.template.set('strength', 0.5);
    series.data.setAll([data]);
    series.appear(1000, 100);
  }

  renderRadarChart(root: am5.Root, data: any) {
    const chart = root.container.children.push(
      am5radar.RadarChart.new(root, {
        panX: false,
        panY: false,
        wheelX: 'none',
        wheelY: 'none',
      })
    );

    const xAxis = chart.xAxes.push(
      am5xy.CategoryAxis.new(root, {
        categoryField: 'category',
        renderer: am5radar.AxisRendererCircular.new(root, {}),
      })
    );

    const yAxis = chart.yAxes.push(
      am5xy.ValueAxis.new(root, {
        renderer: am5radar.AxisRendererRadial.new(root, {}),
      })
    );

    xAxis.data.setAll(data);

    const series = chart.series.push(
      am5radar.RadarLineSeries.new(root, {
        xAxis: xAxis,
        yAxis: yAxis,
        valueYField: 'value',
        categoryXField: 'category',
        fill: am5.color(0x67b7dc),
        stroke: am5.color(0x67b7dc),
        tooltip: am5.Tooltip.new(root, {labelText: '{valueY}'}),
      })
    );
    series.data.setAll(data);
  }

  protected readonly console = console;
}
