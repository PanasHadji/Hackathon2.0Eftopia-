import {AfterViewInit, Component} from '@angular/core';
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
    searchCAseDetailsQuery: string = '';
    selectedLanguage: any;
    selectedCourt: any;
    startDate: Date | null = null;
    endDate: Date | null = null
    article: string = '';
    displayInfo: boolean = false;

    languages = [{name: 'English'}, {name: 'Greek'}, {name: 'French'}];
    courts = [{name: 'Court 1'}, {name: 'Court 2'}, {name: 'Court 3'}];


    onSearch() {
        console.log('Searching for:', this.searchQuery);
    }

    clearAll() {
        this.displayInfo = true;
    }

    courtCases = [
        {
            id: 1,
            caseName: 'Case of Immigration Policy',
            caseNumber: '2023-IM-001',
            summary: 'A case regarding the recent changes in immigration policies and their legal implications.',
            verdict: 'In favor of the plaintiff.',
            date: '2023-05-12',
            categories: [
                {
                    name: 'Immigration Law',
                    value: 35,
                    children: [
                        {
                            name: 'Visa Policy',
                            value: 20,
                            children: [
                                {name: 'Temporary Visas', value: 15},
                                {name: 'Permanent Visas', value: 5}
                            ]
                        },
                        {
                            name: 'Refugee Law',
                            value: 15,
                            children: [
                                {name: 'Asylum Seekers', value: 10},
                                {name: 'Resettlement Programs', value: 5}
                            ]
                        }
                    ]
                },
                {
                    name: 'Financial Law',
                    value: 45,
                    children: [
                        {
                            name: 'Taxation',
                            value: 25,
                            children: [
                                {name: 'Corporate Taxation', value: 10},
                                {name: 'Personal Taxation', value: 15}
                            ]
                        },
                        {
                            name: 'Investment Law',
                            value: 20,
                            children: [
                                {name: 'Stock Market Regulation', value: 10},
                                {name: 'Private Equity', value: 10}
                            ]
                        }
                    ]
                },
                {
                    name: 'Criminal Law',
                    value: 20,
                    children: [
                        {
                            name: 'White-collar Crimes',
                            value: 10,
                            children: [
                                {name: 'Fraud', value: 5},
                                {name: 'Embezzlement', value: 5}
                            ]
                        },
                        {
                            name: 'Violent Crimes',
                            value: 10,
                            children: [
                                {name: 'Assault', value: 5},
                                {name: 'Murder', value: 5}
                            ]
                        }
                    ]
                }
            ],
            categoryPercentages: [
                {category: 'Antitrust Law', value: 55},
                {category: 'Corporate Law', value: 30},
                {category: 'Technology Law', value: 15},
            ],
            radarData: [
                {category: 'Antitrust Law', value: 80},
                {category: 'Corporate Law', value: 60},
                {category: 'Technology Law', value: 50},
            ],
        },
        {
            id: 2,
            caseName: 'Financial Crimes and Tax Evasion',
            caseNumber: '2023-FC-002',
            summary: 'A case investigating the involvement of corporate entities in large-scale tax evasion activities.',
            verdict: 'In favor of the defendant.',
            date: '2023-06-15',
            categories: [
                {
                    name: 'Financial Law',
                    value: 60,
                    children: [
                        {
                            name: 'Corporate Tax Evasion',
                            value: 35,
                            children: [
                                {name: 'Offshore Accounts', value: 20},
                                {name: 'Shell Companies', value: 15}
                            ]
                        },
                        {
                            name: 'Money Laundering',
                            value: 25,
                            children: [
                                {name: 'International Laundering', value: 15},
                                {name: 'Domestic Laundering', value: 10}
                            ]
                        }
                    ]
                },
                {
                    name: 'Corporate Law',
                    value: 25,
                    children: [
                        {
                            name: 'Corporate Governance',
                            value: 15,
                            children: [
                                {name: 'Board of Directors', value: 8},
                                {name: 'Executive Compensation', value: 7}
                            ]
                        },
                        {
                            name: 'Business Compliance',
                            value: 10,
                            children: [
                                {name: 'Regulatory Compliance', value: 5},
                                {name: 'Internal Audits', value: 5}
                            ]
                        }
                    ]
                },
                {
                    name: 'Criminal Law',
                    value: 15,
                    children: [
                        {
                            name: 'Fraud',
                            value: 10,
                            children: [
                                {name: 'Ponzi Schemes', value: 6},
                                {name: 'Tax Fraud', value: 4}
                            ]
                        },
                        {
                            name: 'Bribery',
                            value: 5,
                            children: [
                                {name: 'Corporate Bribery', value: 3},
                                {name: 'Government Bribery', value: 2}
                            ]
                        }
                    ]
                }
            ],
            categoryPercentages: [
                {category: 'Antitrust Law', value: 55},
                {category: 'Corporate Law', value: 30},
                {category: 'Technology Law', value: 15},
            ],
            radarData: [
                {category: 'Antitrust Law', value: 80},
                {category: 'Corporate Law', value: 60},
                {category: 'Technology Law', value: 50},
            ],
        },
        // Additional cases follow the same structure...
    ];

    selectedChartType: { [key: number]: string } = {};
    chartOptions = [
        {label: 'Pie Chart', icon: 'pi pi-chart-pie'},
        {label: 'Radar Chart', icon: 'pi pi-compass'},
        {label: 'Force-Directed Tree', icon: 'pi pi-sitemap'},
    ];

    constructor() {
    }

    ngAfterViewInit() {
        this.courtCases.forEach((courtCase) => {
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
        return this.courtCases.find((courtCase) => courtCase.id === caseId)!;
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
            children: categories.map((category) => ({
                name: category.name,
                value: category.value,
                children: category.children.map((subcategory) => ({
                    name: subcategory.name,
                    value: subcategory.value,
                    children: subcategory.children.map((subSubcategory) => ({
                        name: subSubcategory.name,
                        value: subSubcategory.value
                    }))
                }))
            }))
        };

        const container = root.container.children.push(
            am5.Container.new(root, {
                width: am5.percent(100),
                height: am5.percent(100),
                layout: root.verticalLayout,
            })
        );

        const series = container.children.push(
            am5hierarchy.ForceDirected.new(root, {
                singleBranchOnly: false,
                downDepth: 3,
                topDepth: 1,
                initialDepth: 1,
                valueField: 'value',
                categoryField: 'name',
                childDataField: 'children',
                idField: 'name',
                linkWithField: 'linkWith',
                manyBodyStrength: -10,
                centerStrength: 0.8,
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
}
