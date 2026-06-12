(function(){
  'use strict';

  // Module maps: [title, lessons[]]
  var modules = {
    'module-0': {title: 'Модуль 0 — Введение', lessons:[
      ['lesson-0-1.html','0.1 — Что такое гипноз на самом деле'],
      ['lesson-0-2.html','0.2 — Как работает сознание и подсознание'],
      ['lesson-0-3.html','0.3 — Кому подходит гипноз. Тест на внушаемость'],
      ['lesson-0-4.html','0.4 — Структура курса и чего ожидать']
    ]},
    'module-1': {title: 'Модуль 1 — Базовые техники', lessons:[
      ['lesson-1-1.html','1.1 — Гипнотический договор и подготовка'],
      ['lesson-1-2.html','1.2 — Каталепсия век и body scan'],
      ['lesson-1-3.html','1.3 — Фракцинация и проверка руки'],
      ['lesson-1-4.html','1.4 — Амнезия чисел и порог сомнамбулизма'],
      ['lesson-1-5.html','1.5 — Проверки: каталепсия век и анальгезия'],
      ['lesson-1-6.html','1.6 — Сокращённые версии и углубление']
    ]},
    'module-2': {title: 'Модуль 2 — Стабилизация', lessons:[
      ['lesson-2-1.html','2.1 — Стабилизация сомнамбулизма'],
      ['lesson-2-2.html','2.2 — Скрытый тест фракцинацией'],
      ['lesson-2-3.html','2.3 — Работа с сопротивлением'],
      ['lesson-2-4.html','2.4 — Прямые внушения: базовый протокол'],
      ['lesson-2-5.html','2.5 — Пост-гипнотическое окно']
    ]},
    'module-3': {title: 'Модуль 3 — Мгновенный гипноз', lessons:[
      ['lesson-3-1.html','3.1 — Четыре принципа мгновенного наведения'],
      ['lesson-3-2.html','3.2 — Быстрое наведение через руку'],
      ['lesson-3-3.html','3.3 — Наведение стоя и баланс'],
      ['lesson-3-4.html','3.4 — Вербальный шок и шок от отсутствия шока'],
      ['lesson-3-5.html','3.5 — Феномены в быстром гипнозе'],
      ['lesson-3-6.html','3.6 — Когда использовать: контекст и безопасность']
    ]},
    'module-4': {title: 'Модуль 4 — Феномены', lessons:[
      ['lesson-4-1.html','4.1 — Что такое феномены и зачем они нужны'],
      ['lesson-4-2.html','4.2 — Каталепсия и анальгезия'],
      ['lesson-4-3.html','4.3 — Амнезия: виды и техники'],
      ['lesson-4-4.html','4.4 — Постгипнотические внушения и реиндукция'],
      ['lesson-4-5.html','4.5 — Галлюцинации с открытыми и закрытыми глазами'],
      ['lesson-4-6.html','4.6 — Введение в регрессию']
    ]},
    'module-5': {title: 'Модуль 5 — Терапия', lessons:[
      ['lesson-5-1.html','5.1 — Три вопроса клиенту'],
      ['lesson-5-2.html','5.2 — Четыре конструкции построения внушения'],
      ['lesson-5-3.html','5.3 — Закон компаундинга и усиление'],
      ['lesson-5-4.html','5.4 — Прямое внушение vs регрессия'],
      ['lesson-5-5.html','5.5 — Структура сессии и контекст работы']
    ]},
    'module-6': {title: 'Модуль 6 — Продвинутый уровень', lessons:[
      ['lesson-6-1.html','6.1 — Эстрадный гипноз'],
      ['lesson-6-2.html','6.2 — «Цыганский гипноз»'],
      ['lesson-6-3.html','6.3 — Трудные клиенты и ситуации'],
      ['lesson-6-4.html','6.4 — Скорость vs глубина'],
      ['lesson-6-5.html','6.5 — Этика и границы']
    ]}
  };

  var path = window.location.pathname;
  var moduleMatch = path.match(/modules\/(module-\d)/);
  if(!moduleMatch) return;
  var modKey = moduleMatch[1];
  var mod = modules[modKey];
  if(!mod) return;

  var currentFile = path.split('/').pop();
  var currentIndex = -1;
  for(var i=0;i<mod.lessons.length;i++){
    if(mod.lessons[i][0] === currentFile){ currentIndex = i; break; }
  }
  if(currentIndex < 0) currentIndex = 0;

  var total = mod.lessons.length;
  var pct = Math.round((currentIndex+1)/total*100);

  // Build HTML
  var html = '<div class="module-progress">' +
    '<div class="module-progress-bar"><div class="module-progress-fill" style="width:'+pct+'%"></div></div>' +
    '<div class="module-progress-text">Урок '+(currentIndex+1)+' из '+total+' · '+pct+'%</div>' +
    '</div>' +
    '<ul class="lesson-sidebar-list">';

  for(var j=0;j<mod.lessons.length;j++){
    var cls = 'lesson-sidebar-item';
    if(j === currentIndex) cls += ' current';
    else if(j < currentIndex) cls += ' completed';
    var num = mod.lessons[j][0].replace(/[^\d]/g,'').replace(/^(\d)(\d)$/,'$1.$2');
    html += '<li class="'+cls+'"><a href="'+mod.lessons[j][0]+'">'+
      '<span class="lesson-sidebar-num">'+num+'</span>'+
      '<span class="lesson-sidebar-title">'+mod.lessons[j][1]+'</span>'+
      '</a></li>';
  }
  html += '</ul>';

  // Inject into sidebar
  var sidebar = document.querySelector('.lesson-sidebar');
  if(sidebar) sidebar.innerHTML = html;

  // Inject into mobile panel
  var mobilePanel = document.querySelector('.sidebar-mobile-panel');
  if(mobilePanel) mobilePanel.innerHTML = html;

  // Update toggle button text
  var toggleBtn = document.querySelector('.sidebar-toggle');
  if(toggleBtn){
    toggleBtn.textContent = mod.title + ' · ' + (currentIndex+1) + ' из ' + total;
  }

  window.toggleSidebar = function(){
    var btn = document.querySelector('.sidebar-toggle');
    var panel = document.querySelector('.sidebar-mobile-panel');
    if(!btn || !panel) return;
    btn.classList.toggle('open');
    panel.classList.toggle('open');
  };
})();
