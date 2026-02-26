if (typeof document$ !== "undefined") {
  document$.subscribe(function() {
    // Spec-Weaverが生成したテーブル (.datatable) を対象にDataTablesを適用
    $('article table.datatable:not(.dataTable)').each(function() {
      $(this).DataTable({
        searching: true,
        paging: false,
        info: false,
        order: [], // 初期ソートを無効化
        
        initComplete: function () {
          this.api().columns().every(function () {
            var column = this;
            var headerText = $(column.header()).text().trim();
            
            // フィルタ対象のカラムを指定
            var dropdownColumns = ['ステータス', 'Status', 'レベル', 'Level', '親', 'Parent', '子', 'Child', '兄弟', 'Sibling', '実装状況', '状態'];
            
            if (dropdownColumns.includes(headerText)) {
              var select = $('<select style="display:block; margin-top:4px; width:100%; font-weight:normal;"><option value="">全て</option></select>')
                .appendTo($(column.header()))
                .on('click', function(e) {
                  e.stopPropagation(); // ソートのトリガーを防止
                })
                .on('change', function () {
                  var val = $.fn.dataTable.util.escapeRegex($(this).val());
                  column.search(val ? '^' + val + '$' : '', true, false).draw();
                });

              column.data().unique().sort().each(function (d, j) {
                var textValue = $('<div>').html(d).text().trim() || d;
                if (textValue && textValue !== '-') {
                  if (select.find('option[value="' + textValue + '"]').length === 0) {
                    select.append('<option value="' + textValue + '">' + textValue + '</option>');
                  }
                }
              });
            }
          });
        }
      });
    });
  });
}
