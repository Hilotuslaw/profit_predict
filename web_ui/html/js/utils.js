// 自定义alert函数，带回调
function alert(data, callback) { //回调函数
    var alert_bg = document.createElement('div');
    var alert_box = document.createElement('div');
    var alert_text = document.createElement('div');
    var alert_btn = document.createElement('div');
    var textNode = document.createTextNode(data ? data : '');
    var btnText = document.createTextNode('确 定');

    // 控制样式
    css(alert_bg, {
        'position': 'fixed',
        'top': '0',
        'left': '0',
        'right': '0',
        'bottom': '0',
        'background-color': 'rgba(0, 0, 0, 0.1)',
        'z-index': '999999999'
    });

    css(alert_box, {
        'width': '270px',
        'max-width': '90%',
        'font-size': '16px',
        'text-align': 'center',
        'background-color': '#fff',
        'border-radius': '15px',
        'position': 'absolute',
        'top': '50%',
        'left': '50%',
        'transform': 'translate(-50%, -50%)'
    });

    css(alert_text, {
        'padding': '10px 15px',
        'border-bottom': '1px solid #ddd'
    });

    css(alert_btn, {
        'padding': '10px 0',
        'color': '#007aff',
        'font-weight': '600',
        'cursor': 'pointer'
    });

    // 内部结构套入
    alert_text.appendChild(textNode);
    alert_btn.appendChild(btnText);
    alert_box.appendChild(alert_text);
    alert_box.appendChild(alert_btn);
    alert_bg.appendChild(alert_box);

    // 整体显示到页面内
    document.getElementsByTagName('body')[0].appendChild(alert_bg);

    // 确定绑定点击事件删除标签
    alert_btn.onclick = function() {
        alert_bg.parentNode.removeChild(alert_bg);
        if (typeof callback === 'function') {
            callback(); //回调
        }
    }
}

function css(targetObj, cssObj) {
    var str = targetObj.getAttribute("style") ? targetObj.getAttribute('style') : '';
    for (var i in cssObj) {
        str += i + ':' + cssObj[i] + ';';
    }
    targetObj.style.cssText = str;
}


// 汇总求和一列
var SUMCOL = function(instance, columnId) {
    var total = 0;
    for (var j = 0; j < instance.options.data.length; j++) {
        if (Number(instance.records[j][columnId].innerHTML)) {
            total += Number(instance.records[j][columnId].innerHTML);
        }
    }
    return total;
};

// 刷新active状态标记
var active_fresh = function(li_self, li_arr) {
    li_self.className = "active";
    for (var i=0; i<li_arr.length; i++) {
        if (li_arr[i] != li_self) {
            li_arr[i].className = "";
        }
    }
};

// 获取当前时间并格式化
var getNowFormatDate = function() {
    var date = new Date();
    var year = date.getFullYear();
    var month = date.getMonth() + 1;
    var d = date.getDate();
    if(month<10){
        month = "0" + month;
    }
    if(d<10){
        d = "0" + d;
    }
    return year + "-" + month + "-" + d;
};

// 计算一段时间内的所有月份
var getRangeAllMonth = function(start, end) {
    var getDate = function(datestr) {
        var temp = datestr.split("-");
        var date = new Date(temp[0], temp[1]);
        return date;
    };
    var startTime = getDate(start);
    var endTime = getDate(end);
    var dateArr = [];
    while ((endTime.getTime() - startTime.getTime()) >= 0) {
        var year = startTime.getFullYear();
        var month = startTime.getMonth().toString().length == 1 ? "0" + startTime.getMonth().toString() : startTime.getMonth();
        if (month === "00") {
            month = "12";
            year = year - 1;
        } else {
            month = month;
        }
        var day = startTime.getDate().toString().length == 1 ? "0" + startTime.getDate() : startTime.getDate();
        dateArr.push(year + "-" + month);
        startTime.setDate(startTime.getDate() + 1);
    }
    return Array.from(new Set(dateArr));
};

// 计算一段时间内的所有日期
var getRangeAllDate = function(start, end) {
    var getDate = function(datestr) {
        var temp = datestr.split("-");
        var date = new Date(temp[0], Number(temp[1])-1, temp[2]);
        return date;
    };
    var startTime = getDate(start);
    var endTime = getDate(end);
    var dateArr = [];
    while ((endTime.getTime() - startTime.getTime()) >= 0) {
        var year = startTime.getFullYear();
        var month = startTime.getMonth() + 1;
        month = month.toString().length == 1 ? "0" + month.toString() : month;
        var day = startTime.getDate().toString().length == 1 ? "0" + startTime.getDate() : startTime.getDate();
        dateArr.push(year + "-" + month + "-" + day);
        startTime.setDate(startTime.getDate() + 1);
    }
    return dateArr;
};

// 计算当前月份有多少天
function getCountDays(datestr){
    var temp = datestr.split("-");
    var date = new Date(temp[0], Number(temp[1])-1, temp[2]);
    // 获取当前月份
    // 将日期设置为32，表示自动计算为下个月的第几天（这取决于当前月份有多少天）
    date.setDate(32);
    // 返回当前月份的天数
    return 32-date.getDate();
}


// 将json转换为csv
function jsonToCsv(json) {
    var header = "";
    // 遍历循环取出csv头部
    header = Object.keys(json[0]).map(function(key){
       return "\"" + key + "\"";
    }) + "\n"
    // 遍历循环取出数据部
    var body = json.map(function(oneObj) {
      // 每一个json对象
      return Object.keys(oneObj).map(function(attr) {
          return "\"" + oneObj[attr] + "\"";
      }).join(',');
    }).join('\n');
    return header + body;
  }


  // csv下载实现(chrome,fireFox)
  function csvDownload(content, filename) {
    // 创建一个a元素
    var hrefLink = document.createElement('a');
    // 赋予download属性(html5新增属性)
    hrefLink.download = filename;
    hrefLink.style.display = 'none';

    // 利用Blob将字符串转为二进制,参数必须为数组
    var blob = new Blob([content]);
    // 将下载链接指向创建的blob url。
    // url例：blob:null/f046752e-238e-4bf7-ba13-647a2cae8e84
    hrefLink.href = URL.createObjectURL(blob);
    // 这里的appendChild和removeChild是为了兼容FireFox而添加的
    document.body.appendChild(hrefLink);
    hrefLink.click();
    document.body.removeChild(hrefLink);
}

// 解析float数组
function parse_float_arr(arr) {
    var res = new Array();
    arr.forEach((item) => {
        res.push(parseFloat(item));
    });
    return res;
}

// 解析int数组
function parse_int_arr(arr) {
    var res = new Array();
    arr.forEach((item) => {
        res.push(parseInt(item));
    });
    return res;
}


// 创建绘图元素
function create_div_plot() {
    var div_plot = document.createElement("div");
    div_plot.id = "spreadsheet";
    var div_row_1 = document.createElement("div");
    div_row_1.className = "row";
    var div_row_2 = document.createElement("div");
    div_row_2.className = "row";
    var div_row_3 = document.createElement("div");
    div_row_3.className = "row";
    var div_row_4 = document.createElement("div");
    div_row_4.className = "row";
    var div_row_5 = document.createElement("div");
    div_row_5.className = "row";
    var div_row_6 = document.createElement("div");
    div_row_6.className = "row";
    var div_profit_day = document.createElement("div");
    div_profit_day.className = "div";
    div_profit_day.id = "profit_day";
    var div_profit_month = document.createElement("div");
    div_profit_month.className = "div";
    div_profit_month.id = "profit_month";
    var div_install_dau_day = document.createElement("div");
    div_install_dau_day.className = "div";
    div_install_dau_day.id = "install_dau_day";
    var div_install_dau_month = document.createElement("div");
    div_install_dau_month.className = "div";
    div_install_dau_month.id = "install_dau_month";
    var div_arpu_cpi_day = document.createElement("div");
    div_arpu_cpi_day.className = "div";
    div_arpu_cpi_day.id = "arpu_cpi_day";
    var div_arpu_cpi_month = document.createElement("div");
    div_arpu_cpi_month.className = "div";
    div_arpu_cpi_month.id = "arpu_cpi_month";
    var div_revenue_day = document.createElement("div");
    div_revenue_day.className = "div";
    div_revenue_day.id = "revenue_day";
    var div_revenue_month = document.createElement("div");
    div_revenue_month.className = "div";
    div_revenue_month.id = "revenue_month";
    var div_revenue_flow_day = document.createElement("div");
    div_revenue_flow_day.className = "div";
    div_revenue_flow_day.id = "revenue_flow_day";
    var div_revenue_flow_month = document.createElement("div");
    div_revenue_flow_month.className = "div";
    div_revenue_flow_month.id = "revenue_flow_month";
    var div_cost_day = document.createElement("div");
    div_cost_day.className = "div";
    div_cost_day.id = "cost_day";
    var div_cost_month = document.createElement("div");
    div_cost_month.className = "div";
    div_cost_month.id = "cost_month";
    div_row_1.appendChild(div_profit_day);
    div_row_1.appendChild(div_profit_month);
    div_row_2.appendChild(div_install_dau_day);
    div_row_2.appendChild(div_install_dau_month);
    div_row_3.appendChild(div_arpu_cpi_day);
    div_row_3.appendChild(div_arpu_cpi_month);
    div_row_4.appendChild(div_revenue_day);
    div_row_4.appendChild(div_revenue_month);
    div_row_5.appendChild(div_revenue_flow_day);
    div_row_5.appendChild(div_revenue_flow_month);
    div_row_6.appendChild(div_cost_day);
    div_row_6.appendChild(div_cost_month);
    div_plot.appendChild(div_row_1);
    div_plot.appendChild(div_row_2);
    div_plot.appendChild(div_row_3);
    div_plot.appendChild(div_row_4);
    div_plot.appendChild(div_row_5);
    div_plot.appendChild(div_row_6);
    div_plot.style = "height: 100%; width: 100%; overflow: scroll";
    return div_plot;
}