// 折线图
function plot_line(chart_object, title, legend_list, x_list, y_list) {
    var series_tmp = [];
    for (var i=0; i<legend_list.length; i++) {
        series_tmp.push(
            {
                name: legend_list[i],
                type: 'line',
                data: y_list[i]
            }
        );
    };
    var option = {
        title: {
          text: title
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: legend_list
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        toolbox: {
          feature: {
            saveAsImage: {}
          }
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: x_list
        },
        yAxis: {
          type: 'value'
        },
        series: series_tmp
      };
    option && chart_object.setOption(option);
}

// 双y轴折线图
function plot_double_y_line(chart_object, title, legend_list, x_list, y_list_1, y_list_2, name_list_1, name_list_2) {
    var series_tmp = [];
    for (var i=0; i<name_list_1.length; i++) {
        series_tmp.push(
            {
                name: name_list_1[i],
                type: 'line',
                data: y_list_1[i],
                yAxisIndex: 0,
            }
        );
    };
    for (var i=0; i<name_list_2.length; i++) {
        series_tmp.push(
            {
                name: name_list_2[i],
                type: 'line',
                data: y_list_2[i],
                yAxisIndex: 1,
            }
        );
    };
    var option = {
        title: {
          text: title
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: legend_list
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        toolbox: {
          feature: {
            saveAsImage: {}
          }
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: x_list
        },
        yAxis: [
            {
                type: 'value'
            },
            {
                type: 'value'
            },
        ],
        series: series_tmp
      };
    option && chart_object.setOption(option);
}

// 堆叠面积图
function plot_stack_area(chart_object, title, legend_list, x_list, y_list) {
    var series_tmp = [];
    for (var i=0; i<legend_list.length; i++) {
        series_tmp.push(
            {
                name: legend_list[i],
                type: 'line',
                areaStyle: {},
                emphasis: {
                    focus: 'series'
                },
                data: y_list[i]
            }
        );
    };
    var option = {
        title: {
          text: title
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'cross',
              label: {
                backgroundColor: '#6a7985'
              }
            }
        },
        legend: {
          data: legend_list
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        toolbox: {
          feature: {
            saveAsImage: {}
          }
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: x_list
        },
        yAxis: {
          type: 'value'
        },
        series: series_tmp
      };
    option && chart_object.setOption(option);
}