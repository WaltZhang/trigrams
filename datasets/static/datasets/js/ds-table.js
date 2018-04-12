function resetTable(selector) {
    $(selector).find('thead tr').remove();
    $(selector).find('tbody tr').remove();
}

function addColGroup(cols, selector) {
    if (typeof cols != 'object') {
        cols = JSON.parse(cols);
    }
    for (var i = 0; i < cols.length; i++) {
        var colGroup$ = $('<colgroup/>');
        $(selector).append(colGroup$);
    }
}

function buildTableHeader(columnList, selector) {
    var columnSet = [];
    var headerTr$ = $('<tr/>');

    if (typeof columnList != 'object') {
        columnList = JSON.parse(columnList);
    }
    for (var i in columnList) {
        var key = columnList[i];
        headerTr$.append($('<th/>').html(key));
    }
    $(selector).append(headerTr$);
}

function buildTableBody(bodyList, selector) {
    if (typeof bodyList != 'object') {
        bodyList = JSON.parse(bodyList);
    }
    for (var i in bodyList) {
        var row$ = $('<tr/>');
        for (var j in bodyList[i]) {
            var cellValue = bodyList[i][j];
            if (cellValue == null)
                cellValue = "";
            row$.append($('<td/>').html(cellValue));
        }
        $(selector).append(row$);
    }
}
