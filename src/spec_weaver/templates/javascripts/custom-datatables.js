/**
 * Spec-Weaver DataTables Initialization
 */
function initDataTables() {
  console.log("Spec-Weaver: Initializing DataTables...");
  
  // 1. クラス名 ".datatable" で探す
  // 2. もしくは、最初のヘッダーセルが "ID" であるテーブルを探す
  const $tables = $('article table:not(.dataTable)').filter(function() {
    const hasClass = $(this).hasClass('datatable');
    const firstHeader = $(this).find('th').first().text().trim();
    return hasClass || firstHeader === 'ID';
  });
  
  if ($tables.length === 0) {
    console.log("Spec-Weaver: No target tables found by class or header content.");
    return;
  }

  $tables.each(function() {
    console.log("Spec-Weaver: Converting table to DataTable...");
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
            // 既存のセレクトボックスがあれば削除（重複防止）
            $(column.header()).find('select').remove();

            var select = $('<select style="display:block; margin-top:4px; width:100%; font-weight:normal; color: inherit; background-color: var(--md-code-bg-color); border: 1px solid var(--md-typeset-table-color);"><option value="">全て</option></select>')
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
}

// MkDocs Material のインスタントロード対応
if (typeof document$ !== "undefined") {
  document$.subscribe(function() {
    initDataTables();
  });
} else {
  $(document).ready(function() {
    initDataTables();
  });
}
