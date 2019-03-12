var omega = (function(){
    var myOmega = {};

    var currentPage = 'home';
    var googleLibReady = false;

    myOmega.monitor = (function(){
        var myMonitor = {}

        var libReady = false;
        var started = false;

        var optionsPower = null;
        var optionsRPM = null;
        var optionsAvail = null;
        var optionsFeed = null;

        var chartRPM = null;
        var chartPower = null;
        var chartAvail = null;
        var chartFeed = null;

        var dataAvail = null;
        var dataPower = null;
        var dataRPM = null;
        var dataFeed = null;

        var intervalId = null;

        var rawFeedData = [];

        var ledStatus = [false, false, false];

        var resizer = function(){
            if(this.resizeTO){
                clearTimeout(this.resizeTO);
            }

            this.resizeTO = setTimeout(
                function() {
                    $(this).trigger('resizeEnd');
                }
                , 250);
         }

        var requestMonitorData = function (){
            var path = window.location.protocol + "//" + window.location.host + window.location.pathname;

            $.ajax({
                url: path + "requestMonitorData",
                data: [],
                type: 'POST',
                success: function(response) {
                    var json = JSON.parse(response);
                    if(json != null)
                    {
                        updateData(json);
                    }
                },
                error: function(error) {
                    console.log(error);
                },
                timeout: 999
            });
        }

        var initCharts = function() {
            dataPower = google.visualization.arrayToDataTable([
                ['Label', 'Value'],
                ['Power', 0]
            ]);

            dataRPM = google.visualization.arrayToDataTable([
                ['Label', 'Value'],
                ['RPM', 0]
            ]);

            dataAvail = google.visualization.arrayToDataTable([
                ['', '%', { role: 'style' }],
                ['Availability (%)', 40, 'green'],
                ['Rate (%)', 60, 'blue']
            ]);

            dataFeed = google.visualization.arrayToDataTable([
                ['Time(s)', 'X-Axis', 'Y-Axis', 'Z-Axis']
            ]);

            optionsPower = {
                redFrom: 80, redTo: 100,
                yellowFrom:60, yellowTo: 80,
                greenFrom:0, greenTo:60,
                minorTicks: 10,
                majorTicks: ['0','20','40','60','80','100'],
                max:100,
                min: 0,
                animation: {
                    easing: 'out'
                }
            };

            optionsRPM = {
                redFrom: 12, redTo: 15,
                yellowFrom:9, yellowTo: 12,
                minorTicks: 3,
                majorTicks: ['0','3','6','9','12','15'],
                max:15,
                min: 0,
                animation: {
                    easing: 'out'
                }
            };

            optionsAvail = {
                bars: 'horizontal',
                hAxis: {
                    viewWindow: {
                        min:0,
                        max:100
                        },
                    ticks: ['10', '20', '30', '40', '50', '60', '70', '80', '90', '100'],
                },

                legend: {
                    position: 'none'
                },
                fontSize: 14,
            };

            optionsFeed = {
                viewWindow:{
                    max: 60,
                    min: 0
                },
                hAxis:{
                    title: 'seconds',
                    ticks: [0,5,10,15,20,25,30,35,40,45,50,55,60]
                },
                vAxis:{
                    title: '(%)',
                    ticks: [0,10,20,30,40,50,60,70,80,90,100]
                }
             }

            chartRPM = new google.visualization.Gauge(document.getElementById('gauge-rpm'));
            chartPower = new google.visualization.Gauge(document.getElementById('gauge-power'));
            chartAvail = new google.charts.Bar(document.getElementById('avail-chart'));
            chartFeed = new google.visualization.LineChart(document.getElementById('feed-chart'));

            google.visualization.events.addListener(chartAvail, 'error', errorHandler);
            google.visualization.events.addListener(chartFeed, 'error', errorHandler);

            function errorHandler(errorMessage) {
                //curisosity, check out the error in the console
                console.log(errorMessage);

                //simply remove the error, the user never see it
                google.visualization.errors.removeError(errorMessage.id);
            }
        }

        var drawCharts = function(){
            chartRPM.draw(dataRPM, optionsRPM);
            chartPower.draw(dataPower, optionsPower);
            chartAvail.draw(dataAvail, google.charts.Bar.convertOptions(optionsAvail));
            chartFeed.draw(dataFeed, optionsFeed);
        }

        var updateElementText = function(id, value){
            document.getElementById(id).innerHTML = value;
        }

        var updateData = function(json){
            dataPower.setValue(0, 1, json['spindle_load']);
            chartPower.draw(dataPower, optionsPower);

            dataRPM.setValue(0, 1, json['spindle_speed']);
            chartRPM.draw(dataRPM, optionsRPM);

            updateElementText('cutting-time', json['cutting_time']);
            updateElementText('operating-time', json['operating_time']);
            updateElementText('run-time', json['run_time']);
            updateElementText('poweron-time', json['poweron_time']);
            updateElementText('parts-required', json['parts_required']);
            updateElementText('parts-count', json['parts_count']);

            updateElementText('xaxis', json['posx']);
            updateElementText('yaxis', json['posy']);
            updateElementText('zaxis', json['posz']);

            updateElementText('xaxis-vel', json['velx'].toFixed(3));
            updateElementText('yaxis-vel', json['vely'].toFixed(3));
            updateElementText('zaxis-vel', json['velz'].toFixed(3));

            updateElementText('parts-hour', json['parts_hour'])

            addFeedData(json['velx'], json['vely'], json['velz']);
            updateLed(json['feedrate']);
            updateAlarm(json['alarm_number'], json['alarm_high']);
            updateAvailChart(json['avail'], json['feedrate'])

        }

        var updateAvailChart = function(avail, rate){
            dataAvail = google.visualization.arrayToDataTable([
                ['', '%', { role: 'style' }],
                ['Availability (%)', avail*100, 'green'],
                ['Rate (%)', rate, 'blue']
            ]);
            chartAvail.draw(dataAvail, google.charts.Bar.convertOptions(optionsAvail));
        }

        var addFeedData = function(x, y, z){
            var dataFeed = new google.visualization.DataTable();
            dataFeed.addColumn('number', 'Time(s)');
            dataFeed.addColumn('number', 'X-Axis');
            dataFeed.addColumn('number', 'Y-Axis');
            dataFeed.addColumn('number', 'Z-Axis');

            if(rawFeedData.length > 60)
            {
                rawFeedData.shift();
            }

            rawFeedData.push([0, x, y, z]);

            for(var idx = 0; idx < rawFeedData.length; idx++)
            {
                rawFeedData[idx][0] = idx;
            }

            dataFeed.addRows(rawFeedData);
            chartFeed.draw(dataFeed, optionsFeed);
        }

        var updateLed = function(value){
            var newStatus = null;
            var div = null;
            var bg = null;
            var shadow = null;

            /* RED */
            if(value < 40){
                newStatus = [false, false, true];
            }
            /* YELLOW */
            else if(value >= 40 && value < 80){
                newStatus = [false, true, false];
            }
            /* GREEN */
            else{
                newStatus = [true, false, false];
            }

            for (var idx = 0; idx < ledStatus.length; idx++){
                if(newStatus[idx] != ledStatus[idx]){
                    switch(idx){
                        case 0:
                            div = document.getElementById('green-led');
                            if(newStatus[idx]){
                                bg = "#00ff00";
                                shadow = "0 -1px 15px 6px #00ff00, inset #600 0 -1px 9px, #F00 0 2px 12px";
                            }
                            else {
                                bg = "#006d01";
                                shadow = "0 -1px 5px 1px #444444, inset #444444 0 -1px 9px, #444444 0 2px 12px";
                            }
                            break;

                        case 1:
                            div = document.getElementById('yellow-led');
                            if(newStatus[idx]){
                                bg = "#fff000";
                                shadow = "0 -1px 15px 6px #fff000, inset #600 0 -1px 9px, #F00 0 2px 12px";
                            }
                            else {
                                bg = "#6d6d00";
                                shadow = "0 -1px 5px 1px #444444, inset #444444 0 -1px 9px, #444444 0 2px 12px";
                            }
                            break;

                        case 2:
                            div = document.getElementById('red-led');
                            if(newStatus[idx]){
                                bg = "#ff0000";
                                shadow = "0 -1px 15px 6px #ff0000, inset #600 0 -1px 9px, #F00 0 2px 12px";
                            }
                            else {
                                bg = "#6d0000";
                                shadow = "0 -1px 5px 1px #444444, inset #444444 0 -1px 9px, #444444 0 2px 12px";
                            }
                            break;
                    }

                    div.style.backgroundColor = bg;
                    div.style.boxShadow = shadow;
                }
            }

            ledStatus = newStatus;
        }

        var updateAlarm = function(number, high){
            var divNum = document.getElementById("alarm-number-row");
            var divHigh = document.getElementById("alarm-high-row");

            if(number == 0){
                divNum.style.display = "none";
            }
            else{
                updateElementText("alarm-number", number);
                divNum.style.display = "block";
            }

            if(high == 0){
                divHigh.style.display = "none";
            }
            else{
                updateElementText("alarm-high", high);
                divHigh.style.display = "block";
            }
        }

        myMonitor.startMonitor = function (){
            if(!started){
                started = true;

                initCharts();
                drawCharts();

                $(window).bind('resizeEnd', function() {
                    drawCharts();
                 });

                $(window).resize(resizer);

                intervalId = setInterval(requestMonitorData, 1000);
             }
        }

        myMonitor.stopMonitor = function(){
            if(started)
            {
                clearInterval(intervalId);
                $(window).off("resize", resizer);
                started = false;
            }
        }

        return myMonitor;
    })()

    myOmega.mes = (function(){
        var myMES = {}

        var reportLoaded = true;
        var started = false;

        var selectedDate = null;
        var type = "day";

        var mesData = null;

        var resizer = function(){
            if(this.resizeTO){
                clearTimeout(this.resizeTO);
            }

            this.resizeTO = setTimeout(
                function() {
                    $(this).trigger('resizeEnd');
                }
                , 250);
        }

        var drawRadarChart = function(){
            var data = {
                labels: ["Disponibilidade", "Desempenho", "Qualidade"],
                datasets: [
                    {
                        label: "My First dataset",
                        backgroundColor: "rgba(179,181,198,0.2)",
                        borderColor: "rgba(179,181,198,1)",
                        pointBackgroundColor: "rgba(179,181,198,1)",
                        pointBorderColor: "#fff",
                        pointHoverBackgroundColor: "#fff",
                        pointHoverBorderColor: "rgba(179,181,198,1)",
                        data: [
                            mesData.index.avail.toFixed(3),
                            mesData.index.perf.toFixed(3),
                            mesData.index.quality.toFixed(3)
                        ]
                    }
                ]
            };

            var options = {
                scale: {
                    ticks: {
                        min: 0,
                        max: 1
                    },
                    pointLabels: {
                        fontSize: 14
                    },
                },

                legend: {
                    display: false
                }
            };

            var ctx = document.getElementById("radarChart");
            var myRadarChart = new Chart(ctx, {
                type: 'radar',
                data: data,
                options: options
            });
        }

        var drawBarChart = function(){
            var data = {
                labels: ["Turno 1", "Turno 2", "Turno 3"],
                datasets: [
                    {
                        label: "Tempo de operação",
                        backgroundColor: [
                            'rgba(43, 238, 139, 0.5)',
                            'rgba(43, 238, 139, 0.5)',
                            'rgba(43, 238, 139, 0.5)'
                        ],
                        borderColor: [
                            'rgba(43, 238, 139, 1)',
                            'rgba(43, 238, 139, 1)',
                            'rgba(43, 238, 139, 1)'
                        ],
                        borderWidth: 1,
                        data: [
                            mesData.prodTimeTotal[0][0]/60,
                            mesData.prodTimeTotal[1][0]/60,
                            mesData.prodTimeTotal[2][0]/60
                        ]
                    },
                    {
                        label: "Tempo em parada",
                        backgroundColor: [
                            'rgba(254, 8, 61, 0.8)',
                            'rgba(254, 8, 61, 0.8)',
                            'rgba(254, 8, 61, 0.8)'
                        ],
                        borderColor: [
                            'rgba(254, 8, 61, 1)',
                            'rgba(254, 8, 61, 1)',
                            'rgba(254, 8, 61, 1)'
                        ],
                        borderWidth: 1,
                        data: [
                            mesData.prodTimeTotal[0][1]/60,
                            mesData.prodTimeTotal[1][1]/60,
                            mesData.prodTimeTotal[2][1]/60
                        ]
                    }
                ]
            };

            var ctx = document.getElementById("barChart");

            var options = {
                legend: {
                    labels:{
                        fontSize: 14
                    }
                }
//                animation: {
//                    hover: {animationDuration: 0},
//                    onProgress: function (animation) {
//                        var chartInstance = this.chart,
//                            ctx = chartInstance.ctx;
//                        ctx.font = Chart.helpers.fontString(14, Chart.defaults.global.defaultFontStyle, Chart.defaults.global.defaultFontFamily);
//                        ctx.textAlign = 'center';
//                        ctx.textBaseline = 'bottom';
//
//                        this.data.datasets.forEach(function (dataset, i) {
//                            var meta = chartInstance.controller.getDatasetMeta(i);
//                            meta.data.forEach(function (bar, index) {
//                                var data = dataset.data[index];
//                                ctx.fillText(data, bar._model.x, bar._model.y - 5);
//                            });
//                        });
//                    }
//                },
//                tooltips: {
//                    enabled: false
//                },
//                showTooltips: false
            }

            var myChart = new Chart(ctx, {
                type: "bar",
                data: data,
                options: options
            });

        }

        var drawPieChart = function(){
            var total_running =
                (mesData.prodTimeTotal[0][0] +
                 mesData.prodTimeTotal[1][0] +
                 mesData.prodTimeTotal[2][0])/60;

            var total_stopped =
                    (mesData.prodTimeTotal[0][1] +
                     mesData.prodTimeTotal[1][1] +
                     mesData.prodTimeTotal[2][1])/60;

            var data = {
                labels: [
                    "Máquina operando",
                    "Máquina parada"
                ],
                datasets: [
                    {
                        data: [total_running, total_stopped],
                        backgroundColor: [
                            'rgba(43, 238, 139, 0.8)',
                            'rgba(254, 8, 61, 0.8)'
                        ],
                        hoverBackgroundColor: [
                            "#2BEE8B",
                            "#FE083D"
                        ]
                    }]
            };

            var ctx = document.getElementById("pieChart");

            new Chart(ctx,{
                type:"doughnut",
                data: data,
                options: {
                    animation:{
                        animateScale:true
                    }
                }
            });
        }

        var drawGoogleTimeChart = function(){
            var timeChartData = [
                {name: "Turno 1", containerId: "googleTimeChartT1", start: {h:6, m:0}, end: {h:14, m:0}},
                {name: "Turno 2", containerId: "googleTimeChartT2", start: {h:14, m:0}, end: {h:22, m:0}},
                {name: "Turno 3", containerId: "googleTimeChartT3", start: {h:22, m:0}, end: {d:1, h:6, m:0}}
            ]

            var drawChart = function(item, index, array){
                var firstMark = false;
                var loadData = function(item, index, arr){
                    if(item.start.d == null){
                        item.start.d = 0;
                    }

                    if(item.end.d == null){
                        item.end.d = 0;
                    }

                    dataTable.addRow([
                        name,
                        item.id,
                        new Date(0,0,item.start.d, item.start.h, item.start.m,0),
                        new Date(0,0,item.end.d, item.end.h, item.end.m,0)
                    ]);

                    if(item.id == ""){
                        if(!firstMark){
                            opts.colors.push("#2BEE8B");
                            firstMark = true;
                        }
                    }
                    else{
                        opts.colors.push("#FE083D");
                    }
                }

                var opts = {
                    colors:[]
                };

                var name = timeChartData[index].name;
                var containerId = timeChartData[index].containerId;

                var container = document.getElementById(containerId);
                var chart = new google.visualization.Timeline(container);
                var dataTable = new google.visualization.DataTable();

                dataTable.addColumn({ type: 'string', id: 'Turno' });
                dataTable.addColumn({ type: 'string', id: 'id' });
                dataTable.addColumn({ type: 'date', id: 'Início' });
                dataTable.addColumn({ type: 'date', id: 'Fim' });

                item.forEach(loadData);

                chart.draw(dataTable, opts);
            }

            mesData.prodTime.forEach(drawChart);
        }

        var updateProdTable = function(){
            $("#prod-table-body").empty();

            var tbody = document.getElementById("prod-table-body");

            var loadData = function(item){

                var addRow = function(item){
                    if(item.id != ""){
                        var tdStop = document.createElement("td");
                        var tdStart = document.createElement("td");
                        var tdEnd = document.createElement("td");
                        var tdDuration = document.createElement("td");
                        var tdReason = document.createElement("td");

                        var momentStart = moment(new Date(0,0,0,item.start.h, item.start.m,0));
                        var momentEnd = moment(new Date(0,0,0,item.end.h, item.end.m,0));
                        var momentDiff = moment.utc(moment(momentEnd.diff(momentStart)));

                        tdStop.innerHTML = item.id;
                        tdStart.innerHTML = momentStart.format("HH:mm");
                        tdEnd.innerHTML = momentEnd.format("HH:mm");
                        tdDuration.innerHTML = momentDiff.format("HH:mm");
                        tdReason.innerHTML = item.reason;

                        var tr = document.createElement("tr");
                        tr.appendChild(tdStop);
                        tr.appendChild(tdStart);
                        tr.appendChild(tdEnd);
                        tr.appendChild(tdDuration);
                        tr.appendChild(tdReason);

                        tbody.appendChild(tr);
                    }
                }

                item.forEach(addRow);
            }

            mesData.prodTime.forEach(loadData);
        }

        var updateData = function(type){
            var e = document.getElementById('scc');
            e.innerHTML = mesData.data.scc;

            e = document.getElementById('cell');
            e.innerHTML = mesData.data.celula;

            e = document.getElementById('resp');
            e.innerHTML = mesData.data.resp;

            var date_str = moment(mesData.data.date_start).locale('pt-br').format('L');

            if(type == 'period'){
                date_str += ' à ';
                date_str += moment(mesData.data.date_end).locale('pt-br').format('L');
            }

            e = document.getElementById('date');
            e.innerHTML = date_str

            e = document.getElementById('pn');
            e.innerHTML = mesData.data.pn;
        }

        var updateProdAmount = function(){
            var e = document.getElementById('amount-t1');
            e.innerHTML = mesData.prodAmount.turn1.toFixed(2);

            e = document.getElementById('amount-t2');
            e.innerHTML = mesData.prodAmount.turn2.toFixed(2);

            e = document.getElementById('amount-t3');
            e.innerHTML = mesData.prodAmount.turn3.toFixed(2);

            e = document.getElementById('amount-total');
            e.innerHTML = mesData.prodAmount.total.toFixed(2);
        }

        var updateOpAmount = function(){
            var e = document.getElementById('op-amount-t1');
            e.innerHTML = mesData.opAmount.turn1.toFixed(2);

            e = document.getElementById('op-amount-t2');
            e.innerHTML = mesData.opAmount.turn2.toFixed(2);

            e = document.getElementById('op-amount-t3');
            e.innerHTML = mesData.opAmount.turn3.toFixed(2);
        }

        var updateIndexes = function(){
            var e = document.getElementById('availability');
            e.innerHTML = mesData.index.avail.toFixed(3);

            e = document.getElementById('performance');
            e.innerHTML = mesData.index.perf.toFixed(3);

            e = document.getElementById('quality');
            e.innerHTML = mesData.index.quality.toFixed(3);

            e = document.getElementById('oee');
            e.innerHTML = mesData.index.oee.toFixed(3);
        }

        var requestData = function(type, date1, date2){
            var path = window.location.protocol + "//" + window.location.host + window.location.pathname;
            var jsonData = null;

            if(type == 'daily'){
                jsonData = {'type': type, 'date': date1};
            }
            else {
                jsonData = {'type': type, 'date-start': date1, 'date-end': date2};
            }

            $.ajax({
                url: path + "requestMESData",
                data: [],
                type: 'POST',
                data: JSON.stringify(jsonData),
                contentType: 'application/json;charset=UTF-8',
                success: function(response) {
                    mesData = JSON.parse(response);
                    if(mesData != null)
                    {
                        if(mesData.ret_code == 0){
                            $("#alert").hide(0);
                            if(omega.isGoogleLibReady() == true){
                                omega.mes.startMES(type);
                            }
                        }
                        else {
                            $("#mes-content").hide();
                            $("#alert").html(mesData.msg)
                            $("#alert").show();
                        }
                    }
                },
                error: function(error) {
                    console.log(error);
                },
                timeout: 10000
            });
        }

        myMES.startMES = function(type){
            started = true;

            $("#mes-content").show(0);

            drawRadarChart();
            drawBarChart();
            drawPieChart();
            updateData(type);
            updateProdAmount();
            updateOpAmount();
            updateIndexes();

            if (type == 'daily'){
                drawGoogleTimeChart();
                updateProdTable();
                $(window).bind('resizeEnd', function() {
                    drawGoogleTimeChart();
                 });

                $(window).resize(resizer);
            }
        }

        myMES.stopMES = function(){
            if(started){
                started = false;
                $(window).off("resize", resizer);
            }
        }

        myMES.isReportLoaded = function(){
            var out = false;

            if (mesData != null){
                out = true;
            }

            return out;
        }

        myMES.loadReport = function(type){
            var date1 = null;
            var date2 = null;

            if(type == 'daily'){
                date1 = $('#datetimepicker').data("DateTimePicker").date().format("YYYY-MM-DD");
                requestData(type, date1);
            }
            else if(type == 'period'){
                date1 = $('#datetimepicker-start').data("DateTimePicker").date().format("YYYY-MM-DD");
                date2 = $('#datetimepicker-end').data("DateTimePicker").date().format("YYYY-MM-DD");
                requestData(type, date1, date2);
            }
        }

        return myMES;
    })()

    myOmega.program = (function(){
        var myProgram = {};

        var uploadTimeoutId = null;

        var list_name = [];

        var downloadSelected = null

        var loadFileTree = function(){
            $('#download-tree').fileTree({ root: './', script: 'listProgram' },
            function(file) {
                $( '#delete-btn' ).prop('disabled', false);
                $( '#download-btn' ).prop('disabled', false);
                downloadSelected = file;
            });
        }

        var handleFileSelect = function(evt) {
            var addRow = function(name)
            {
                $( '#upload-tree' )
                    .append( $('<li class="file ext_exe"><a href="#" rel="/">' + name + '</a></li>') );
            }

            var files = evt.target.files; // FileList object

            for (var i = 0, f; f = files[i]; i++)  {
                addRow(f.name)
            }

            if(files.length > 0){
                $( '#clear-btn' ).prop('disabled', false);
                $( '#send-btn' ).prop('disabled', false);
            }
        }

        myProgram.manageModal = function(){
            var onTimeout = function(){
                $( '#loading-gif' ).hide(0);
                $( '#upload-cancel-btn' ).hide(0);
                $( '#upload-ok-btn' ).show();
                $( '#upload-success' ).show();
            }

            $( '#upload-tree li a' ).each(function( index, elem ) {
                list_name.push(elem.innerHTML);
            })

            if(list_name.length > 0)
            {
                $( '#upload-ok-btn' ).hide(0);
                $( '#upload-success' ).hide(0);
                $( '#loading-gif' ).show(0);
                $( '#upload-cancel-btn' ).show(0);

                $('#myModal').modal('show');

            }
            else{
                $('#myModal').modal('hide');
            }

            var timeout =  Math.floor((Math.random() * 2000) + 2000);
            uploadTimeoutId = setTimeout(onTimeout, timeout);
        }

        myProgram.cancelUpload = function(){
            clearTimeout(uploadTimeoutId);
        }

        myProgram.sendFileList = function(){
            var path = window.location.protocol + "//" + window.location.host + window.location.pathname;

            $.ajax({
                    url: path + "uploadProgram",
                    data: [],
                    type: 'POST',
                    data: JSON.stringify({'file_list': list_name}),
                    contentType: 'application/json;charset=UTF-8',
                    success: function(response) {
                        loadFileTree();
                        myProgram.clearUploadList();
                    },
                    error: function(error) {
                        console.log(error);
                    },
                    timeout: 10000
                });
        }

        myProgram.clearUploadList = function(){
            $( '#upload-tree' ).empty();
            list_name = []
            $( '#clear-btn' ).prop('disabled', true);
            $( '#send-btn' ).prop('disabled', true);
        }

        myProgram.startProgram = function(){
            loadFileTree();

            $( '#clear-btn' ).prop('disabled', true);
            $( '#send-btn' ).prop('disabled', true);
            $( '#delete-btn' ).prop('disabled', true);
            $( '#download-btn' ).prop('disabled', true);

            document.getElementById('files_button').addEventListener('change', handleFileSelect, false);
        }

        return myProgram;
    })()

    myOmega.medicao = (function(){
        var myMedicao = {};

        myMedicao.clearFields = function(){
            $('#medida1').val('');
            $('#medida2').val('');
            $('#medida3').val('');

        }

        return myMedicao;
    })()

    myOmega.googleLibLoaded = function(){
        googleLibReady = true;
        if(currentPage == 'monitor')
        {
            omega.monitor.startMonitor();
        }
        else if(currentPage == 'mes_daily' && omega.mes.isReportLoaded())
        {
            omega.mes.startMES('daily');
        }
    }

    myOmega.isGoogleLibReady = function(){
        return googleLibReady;
    }

    myOmega.requestPage= function(id){
        var path = window.location.protocol + "//" + window.location.host + window.location.pathname;

        $.ajax({
          type: "POST",
          url: path + 'requestPage',
          data: '{"page-id":"' + id + '"}',
          success: post_callback,
          contentType: 'application/json;charset=UTF-8',
          error: function(error) {
            console.log(error);
          }
        });

        $( '.navbar-collapse.in' ).collapse('hide');

        function post_callback(data)
        {
            $( "#page-wrapper" ).html( data );

            currentPage = id;

            if(id == 'monitor'){
                if(omega.isGoogleLibReady() == true){
                    omega.monitor.startMonitor();
                }
            }
            else {
                omega.monitor.stopMonitor();
            }

            if(id == 'mes_daily'){
                $('#datetimepicker').datetimepicker({defaultDate: moment().format(), format: 'LL', locale: 'pt-br', calendarWeeks: true});
                omega.mes.loadReport('daily');
            }
            else if(id == 'mes_period'){
                $('#datetimepicker-start').datetimepicker({defaultDate: moment().add(-1, 'month').format(), format: 'LL', locale: 'pt-br', calendarWeeks: true});
                $('#datetimepicker-end').datetimepicker({defaultDate: moment().format(), format: 'LL', locale: 'pt-br', calendarWeeks: true});
            }
            else {
                omega.mes.stopMES();
            }

            if(id == 'program'){
                omega.program.startProgram();
            }
        }

        return false;
    }

    return myOmega;
})()

$(function(){
    omega.requestPage('home');
    google.charts.load('current', {'packages':['corechart', 'gauge', 'bar', 'timeline']});
    google.charts.setOnLoadCallback(omega.googleLibLoaded);
});
