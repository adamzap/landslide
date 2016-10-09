var Landslide = function () {
  this.$slides = $('.slide');
  this.presenter_view_window = null;

  this.init = function () {
    var n;
    var hash = window.location.hash;

    if (hash === '') {
      n = 1;
    } else if (hash.indexOf('#presenter') !== -1) {
      n = parseInt(hash.replace('#presenter', ''));

      this.presenter_view_window = window;

      $('body').addClass('presenter_view');
    } else {
      n = parseInt(hash.replace('#slide', ''));
    }

    this.$slides.on('click', this.on_slide_click.bind(this));
    $(document).on('keydown', this.on_key_down.bind(this));
    $('#toc a').on('click', this.on_toc_link_click.bind(this));
    $(window).on('message', this.on_window_message.bind(this));

    this.seek_to_slide(n, false);
  };

  this.seek_to_slide = function (n, update_other) {
    this.$current = $('.slide[data-n="' + n + '"]');

    var n = parseInt($current.data('n'));
    var hash_prefix = window.opener ? 'presenter' : 'slide';

    window.location.hash = hash_prefix + n;

    this.$slides.removeClass('far-past past current future far-future p-far');

    this.$slides.slice(0, Math.max(n - 2, 0)).addClass('far-past')
    this.$current.parent().prev().find('.slide').addClass('past');
    this.$current.addClass('current');
    this.$current.parent().next().find('.slide').addClass('future');
    this.$slides.slice(n + 1).addClass('far-future')

    this.highlight_current_toc_link();

    $('title').text($current.find('header').first().text());

    if (window.opener) {
      this.update_presenter_notes();
      this.$slides.slice(n + 2).addClass('p-far')
    }

    if (update_other) {
      this.update_other_page();
    }
  };

  this.update_presenter_notes = function () {
    var $notes_box = $('#current_presenter_notes');

    $notes_box.html($current.find('.presenter_notes').clone());
  };

  this.highlight_current_toc_link = function () {
    $('#toc tr').removeClass('active');
    $('#toc-row-' + $current.data('n')).addClass('active');
  };

  this.update_other_page = function () {
    if (!this.presenter_view_window) {
      return;
    }

    var win = window.opener ? window.opener : this.presenter_view_window

    win.postMessage($current.data('n'), '*');
  };

  this.next_slide = function () {
    if (parseInt($current.data('n')) >= this.$slides.length) {
      return;
    }

    this.seek_to_slide($current.data('n') + 1, true);
  };

  this.prev_slide = function () {
    if (parseInt($current.data('n')) < 2) {
      return;
    }

    this.seek_to_slide($current.data('n') - 1, true);
  };

  this.toggle_notes = function () {
    this.$current.find('.notes').toggle();
  };

  this.toggle_slide_numbers = function () {
    $('.page_number').toggle();
  };

  this.toggle_slide_sources = function () {
    $('.source').toggle();
  };

  this.toggle_toc = function () {
    if ($('#help').hasClass('open')) {
      this.toggle_help();
    }

    $('#toc').toggleClass('open');

    this.update_overview();
  };

  this.toggle_help = function () {
    if ($('#toc').hasClass('open')) {
      this.toggle_toc();
    }

    $('#help').toggleClass('open');
  };

  this.toggle_presenter_view = function () {
    if (window.opener) {
      return;
    }

    if (this.presenter_view_window) {
      this.presenter_view_window.close();
      this.presenter_view_window = null;
    } else {
      var url = window.location.pathname + '#presenter' + $current.data('n');
      var options = 'location=no,toolbar=no,menubar=no';

      this.presenter_view_window = open(url, 'presenter_notes', options);
    }
  };

  this.toggle_3d = function () {
    $('body').toggleClass('three-d');
  };

  this.toggle_overview = function () {
    var active = $('body').hasClass('overview');
    var expanded = $('body').hasClass('expanded');

    $('body').toggleClass('overview');

    this.update_overview();
    this.set_scale(active && expanded ? this.get_expanded_scale() : 1);
  };

  this.update_overview = function () {
    var toc_open = $('#toc').hasClass('open');
    var overview_active = $('body').hasClass('overview');

    if (window.opener) {
      $('body').toggleClass('presenter_view', !overview_active);
    }

    $('.presentation').toggleClass('sidebar-open', toc_open);
  };

  this.get_expanded_scale = function () {
    var el = this.$current[0];

    var sx = el.offsetWidth / window.innerWidth;
    var sy = el.offsetHeight / window.innerHeight;

    return 1 / Math.max(sx, sy);
  };

  this.set_scale = function (scale) {
    $('.slides').css('transform', 'scale(' + scale + ')');
  };

  this.expand_slides = function () {
    var expanded = $('body').hasClass('expanded');
    var new_scale = expanded ? 1 : this.get_expanded_scale();

    this.set_scale(new_scale);

    $('body').toggleClass('expanded');
  };

  this.toggle_context = function () {
    $('.slides').toggleClass('nocontext');
  };

  this.toggle_blank = function () {
    $('#blank').toggle();
  };

  this.overview_only = function (f) {
    return $('body').hasClass('overview') ? f : $.noop;
  };

  this.reject_overview = function (f) {
    return $('body').hasClass('overview') ? $.noop : f;
  };

  this.on_key_down = function (e) {
    var handlers = {
      'ArrowLeft': this.prev_slide,
      'ArrowRight': this.next_slide,
      ' ': this.next_slide,
      'ArrowUp': $.noop,
      'ArrowDown': $.noop,
      'Escape': this.toggle_overview,
      '2': this.toggle_notes,
      'n': this.toggle_slide_numbers,
      't': this.toggle_toc,
      'h': this.toggle_help,
      '.': this.toggle_blank,
      '0': this.toggle_blank,
      'b': this.toggle_blank,
      's': this.toggle_slide_sources,
      'Enter': this.overview_only(this.toggle_overview),
      '3': this.reject_overview(this.toggle_3d),
      'c': this.reject_overview(this.toggle_context),
      'e': this.reject_overview(this.expand_slides),
      'p': this.reject_overview(this.toggle_presenter_view)
    };

    if (handlers[e.key]) {
      e.preventDefault();

      handlers[e.key].bind(this)();
    }
  };

  this.on_slide_click = function (e) {
    var $target = $(e.target);

    if ($target.closest('aside.source').length) {
      return;
    }

    e.preventDefault();

    var n = $target.closest('.slide').data('n');

    this.seek_to_slide(n, true);

    if ($('body').hasClass('overview')) {
      this.toggle_overview();
    }
  }

  this.on_window_message = function (e) {
    this.seek_to_slide(e.originalEvent.data, false);
  };

  this.on_toc_link_click = function (e) {
    e.preventDefault();

    var slide_number = $(e.target).attr('href').replace('#slide', '');

    this.seek_to_slide(slide_number, true);
  };

  this.init();
};
