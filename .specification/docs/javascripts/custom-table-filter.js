if (typeof document$ !== "undefined") {
  document$.subscribe(function() {
    if (!document.getElementById('table-filter-style')) {
      const style = document.createElement('style');
      style.id = 'table-filter-style';
      style.innerHTML = `
        /* 1. テーブルの挙動を「内容優先」に変更 */
        .md-typeset table:not([class]) {
          display: table !important;
          table-layout: auto !important; /* 自動計算に戻す */
          width: 150%;
          min-width: 2000px !important; /* ★ここを大きくするとテーブルが横に広がります */
          margin-bottom: 1rem;
        }

        /* 2. 親要素で横スクロールを許可する */
        .md-typeset__table {
          overflow-x: auto !important;
          -webkit-overflow-scrolling: touch;
        }

        /* ヘッダーのレイアウト調整（折り返し禁止） */
        .filter-th-container {
          display: flex;
          align-items: center;
          justify-content: space-between;
          gap: 8px;
          white-space: nowrap; /* ★ヘッダーテキストの改行を禁止 */
        }

        .filter-select {
          border: none !important;
          background: transparent !important;
          color: var(--md-default-fg-color--light);
          cursor: pointer;
          font-size: 0.75rem !important;
          padding: 0 !important;
          margin: 0 !important;
          appearance: auto !important;
          flex-shrink: 0;
        }

        .th-filtered {
          background-color: var(--md-accent-fg-color--transparent) !important;
        }

        .table-search-input {
          width: 100%;
          padding: 0.6rem;
          margin-bottom: 0.8rem;
          border: 1px solid var(--md-default-fg-color--lightest);
          border-radius: 0.1rem;
          background-color: var(--md-default-bg-color);
          color: var(--md-default-fg-color);
        }
      `;
      document.head.appendChild(style);
    }

    const tables = document.querySelectorAll("article table:not(.processed-table)");

    tables.forEach(function(table) {
      table.classList.add("processed-table");

      // 列ごとの「最小幅」を個別に指定して、内容が潰れないようにする
      const minColWidths = {
        'ID': '100px',
        'タイトル': '350px',
        '親': '120px',
        '子': '180px',
        '兄弟': '120px',
        'カバレッジ': '140px',
        '実装状況': '140px',
        '状態': '100px'
      };

      const headers = table.querySelectorAll('th');
      headers.forEach(th => {
        const txt = th.textContent.trim();
        if (minColWidths[txt]) {
          th.style.minWidth = minColWidths[txt];
        }
      });

      if (typeof Tablesort !== "undefined") {
        new Tablesort(table);
      }

      // --- 以下、フィルタリングロジック（変更なし） ---
      const tbody = table.querySelector('tbody');
      if (!tbody) return;
      const rows = Array.prototype.slice.call(tbody.querySelectorAll('tr'));
      const filters = { text: "", dropdowns: {} };
      const multiValueCols = ['親', 'Parent', '子', 'Child', '兄弟', 'Sibling'];
      const targetCols = multiValueCols.concat(['ステータス', 'Status', 'レベル', 'Level', '状態', '実装状況', 'カバレッジ']);

      const searchInput = document.createElement('input');
      searchInput.className = 'table-search-input';
      searchInput.placeholder = 'キーワードで絞り込み...';
      table.parentNode.insertBefore(searchInput, table);
      searchInput.addEventListener('input', (e) => {
        filters.text = e.target.value.toLowerCase();
        applyFilters();
      });

      function getValues(cell) {
        let values = [];
        const tags = cell.querySelectorAll('span, a, code, li, div');
        if (tags.length > 0) {
          tags.forEach(t => { if(t.textContent.trim()) values.push(t.textContent.trim()); });
        } else {
          const txt = cell.textContent.trim();
          if (txt) values = txt.split(/[,、\s\n]+/).map(s => s.trim());
        }
        return values.filter((v, i, self) => v !== "" && self.indexOf(v) === i);
      }

      headers.forEach((th, index) => {
        const headerText = th.childNodes[0].textContent.trim();
        if (targetCols.indexOf(headerText) !== -1) {
          let allValues = [];
          rows.forEach(row => { allValues = allValues.concat(getValues(row.children[index])); });
          const uniqueValues = [...new Set(allValues)].sort();

          const container = document.createElement('div');
          container.className = 'filter-th-container';
          
          const textSpan = document.createElement('span');
          textSpan.textContent = headerText;
          
          const select = document.createElement('select');
          select.className = 'filter-select';
          select.innerHTML = '<option value=""></option>' + 
            uniqueValues.map(v => `<option value="${v}">${v}</option>`).join('');

          select.addEventListener('click', e => e.stopPropagation());
          select.addEventListener('change', e => {
            filters.dropdowns[index] = { value: e.target.value, isMulti: multiValueCols.indexOf(headerText) !== -1 };
            th.classList.toggle('th-filtered', e.target.value !== "");
            applyFilters();
          });

          th.childNodes[0].textContent = "";
          container.appendChild(textSpan);
          container.appendChild(select);
          th.insertBefore(container, th.firstChild);
        }
      });

      function applyFilters() {
        rows.forEach(row => {
          let isMatch = true;
          if (filters.text && row.textContent.toLowerCase().indexOf(filters.text) === -1) isMatch = false;
          if (isMatch) {
            Object.keys(filters.dropdowns).forEach(idx => {
              const conf = filters.dropdowns[idx];
              if (conf.value && getValues(row.children[idx]).indexOf(conf.value) === -1) isMatch = false;
            });
          }
          row.style.display = isMatch ? '' : 'none';
        });
      }
    });
  });
}
