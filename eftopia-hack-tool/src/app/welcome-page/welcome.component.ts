import {Component, OnInit} from '@angular/core';
import {Router, RouterModule} from '@angular/router';
import {ButtonModule} from 'primeng/button';
import * as am5 from '@amcharts/amcharts5';
import * as am5xy from '@amcharts/amcharts5/xy';
import am5themes_Animated from '@amcharts/amcharts5/themes/Animated';
import {courtCasesData} from './court-year-data';

@Component({
  selector: 'app-welcome',
  standalone: true,
  imports: [RouterModule, ButtonModule],
  template: `
    <div class="main-container">
      <div class="card">
        <h1 class="animated-title">Enhancing Digital Justice</h1>
        <button pButton type="button" label="Start" class="start-button" (click)="goToSearchPage()"></button>
      </div>
      <div class="card">
        <div id="chartdiv"></div>
      </div>
    </div>
  `,
  styles: [`
    .main-container {
      display: flex;
      flex-direction: column;
      justify-content: flex-start;
      align-items: center;
      min-height: 100vh;
      padding: 20px;
      background-color: #f9f9f9;
    }

    .card {
      background: #f9f9f9;
      border-radius: 8px;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
      padding: 20px;
      width: 100%;
      margin: 20px 0;
    }

    .animated-title {
      font-size: 3rem;
      color: #333;
      animation: fadeIn 2s ease-in-out;
      margin-bottom: 20px;
      text-align: center;
    }

    .start-button {
      display: block;
      margin: 0 auto;
      z-index: 2;
    }

    #chartdiv {
      width: 100%;
      height: 500px;
    }

    @keyframes fadeIn {
      from {
        opacity: 0;
      }
      to {
        opacity: 1;
      }
    }
  `]
})
export class WelcomeComponent implements OnInit {
  constructor(private router: Router) {
  }

  ngOnInit(): void {
    this.initializeChart();
  }

  goToSearchPage() {
    this.router.navigate(['./file-search']);
  }

  initializeChart() {
    let root = am5.Root.new("chartdiv");

    root.numberFormatter.setAll({
      numberFormat: "#a",

      bigNumberPrefixes: [
        {number: 1e6, suffix: "M"},
        {number: 1e9, suffix: "B"}
      ],

      smallNumberPrefixes: []
    });

    let stepDuration = 2000;

    root.setThemes([am5themes_Animated.new(root)]);

    let chart = root.container.children.push(am5xy.XYChart.new(root, {
      panX: true,
      panY: true,
      wheelX: "none",
      wheelY: "none",
      paddingLeft: 0
    }));

    chart.zoomOutButton.set("forceHidden", true);
    let yRenderer = am5xy.AxisRendererY.new(root, {
      minGridDistance: 20,
      inversed: true,
      minorGridEnabled: true
    });
    yRenderer.grid.template.set("visible", false);

    let yAxis = chart.yAxes.push(am5xy.CategoryAxis.new(root, {
      maxDeviation: 0,
      categoryField: "network",
      renderer: yRenderer
    }));

    let xAxis = chart.xAxes.push(am5xy.ValueAxis.new(root, {
      maxDeviation: 0,
      min: 0,
      strictMinMax: true,
      extraMax: 0.1,
      renderer: am5xy.AxisRendererX.new(root, {})
    }));

    xAxis.set("interpolationDuration", stepDuration / 10);
    xAxis.set("interpolationEasing", am5.ease.linear);


// Add series
// https://www.amcharts.com/docs/v5/charts/xy-chart/series/
    let series = chart.series.push(am5xy.ColumnSeries.new(root, {
      xAxis: xAxis,
      yAxis: yAxis,
      valueXField: "value",
      categoryYField: "network"
    }));

// Rounded corners for columns
    series.columns.template.setAll({cornerRadiusBR: 5, cornerRadiusTR: 5});

// Make each column to be of a different color
    series.columns.template.adapters.add("fill", function (fill: any, target: any) {
      return chart.get("colors")!.getIndex(series.columns.indexOf(target));
    });

    series.columns.template.adapters.add("stroke", function (stroke: any, target: any) {
      return chart.get("colors")!.getIndex(series.columns.indexOf(target));
    });

// Add label bullet
    series.bullets.push(function () {
      return am5.Bullet.new(root, {
        locationX: 1,
        sprite: am5.Label.new(root, {
          text: "{valueXWorking.formatNumber('#.# a')}",
          fill: root.interfaceColors.get("alternativeText"),
          centerX: am5.p100,
          centerY: am5.p50,
          populateText: true
        })
      });
    });

    let label = chart.plotContainer.children.push(am5.Label.new(root, {
      text: "2002",
      fontSize: "8em",
      opacity: 0.2,
      x: am5.p100,
      y: am5.p100,
      centerY: am5.p100,
      centerX: am5.p100
    }));

    function getSeriesItem(category: any) {
      for (var i = 0; i < series.dataItems.length; i++) {
        let dataItem = series.dataItems[i];
        if (dataItem.get("categoryY") == category) {
          return dataItem;
        }
      }
      return ''
    }

    function sortCategoryAxis() {
      // sort by value
      series.dataItems.sort(function (x: any, y: any) {
        return y.get("valueX") - x.get("valueX");
      });

      // go through each axis item
      am5.array.each(yAxis.dataItems, function (dataItem: any) {
        // get corresponding series item
        let seriesDataItem: any = getSeriesItem(dataItem.get("category"));

        if (seriesDataItem) {
          // get index of series data item
          let index = series.dataItems.indexOf(seriesDataItem);
          // calculate delta position
          let deltaPosition =
            (index - dataItem.get("index", 0)) / series.dataItems.length;
          // set index to be the same as series data item index
          if (dataItem.get("index") != index) {
            dataItem.set("index", index);
            // set deltaPosition instanlty
            dataItem.set("deltaPosition", -deltaPosition);
            // animate delta position to 0
            dataItem.animate({
              key: "deltaPosition",
              to: 0,
              duration: stepDuration / 2,
              easing: am5.ease.out(am5.ease.cubic)
            });
          }
        }
      });
      yAxis.dataItems.sort(function (x, y) {
        return x.get("index")! - y.get("index")!;
      });
    }

    let year = 1995;

    let interval = setInterval(function () {
      year++;

      if (year > 2024) {
        clearInterval(interval);
        clearInterval(sortInterval);
      }

      updateData();
    }, stepDuration);

    let sortInterval = setInterval(function () {
      sortCategoryAxis();
    }, 100);

    function setInitialData() {
      let d = courtCasesData[year];

      for (var n in d) {
        series.data.push({network: n, value: d[n]});
        yAxis.data.push({network: n});
      }
    }

    function updateData() {
      let itemsWithNonZero = 0;

      if (courtCasesData[year]) {
        label.set("text", year.toString());

        am5.array.each(series.dataItems, function (dataItem: any) {
          let category = dataItem.get("categoryY");
          let value = courtCasesData[year][category];

          if (value > 0) {
            itemsWithNonZero++;
          }

          dataItem.animate({
            key: "valueX",
            to: value,
            duration: stepDuration,
            easing: am5.ease.linear
          });
          dataItem.animate({
            key: "valueXWorking",
            to: value,
            duration: stepDuration,
            easing: am5.ease.linear
          });
        });

        yAxis.zoom(0, itemsWithNonZero / yAxis.dataItems.length);
      }
    }

    setInitialData();
    setTimeout(function () {
      year++;
      updateData();
    }, 50);

    series.appear(1000);
    chart.appear(1000, 100);
  }
}
