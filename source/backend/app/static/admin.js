(function () {
  "use strict";

  function toast(message) {
    var node = document.getElementById("toast");
    if (!node) return;
    node.textContent = message;
    node.classList.add("show");
    clearTimeout(node._timer);
    node._timer = setTimeout(function () {
      node.classList.remove("show");
    }, 2600);
  }
  window.toast = toast;

  function initNav() {
    var toggle = document.querySelector("[data-menu-toggle]");
    if (!toggle) return;
    toggle.addEventListener("click", function () {
      document.body.classList.toggle("nav-open");
    });
    document.addEventListener("click", function (event) {
      if (!document.body.classList.contains("nav-open")) return;
      if (event.target.closest("#sidebar") || event.target.closest("[data-menu-toggle]")) return;
      document.body.classList.remove("nav-open");
    });
  }

  function initConfirm() {
    document.querySelectorAll("form[data-confirm]").forEach(function (form) {
      form.addEventListener("submit", function (event) {
        if (!window.confirm(form.getAttribute("data-confirm"))) {
          event.preventDefault();
        }
      });
    });
  }

  function initAlerts() {
    document.querySelectorAll(".alert[data-autohide]").forEach(function (node) {
      setTimeout(function () {
        node.style.transition = "opacity .3s ease";
        node.style.opacity = "0";
        setTimeout(function () { node.remove(); }, 320);
      }, 3200);
    });
  }

  function initEditor() {
    var form = document.getElementById("recipe-form");
    if (!form) return;

    var ingredientTable = document.getElementById("ingredient-table");
    var addIngredient = document.getElementById("add-ingredient");
    var ingredientTemplate = document.getElementById("ingredient-template");
    if (ingredientTable && addIngredient && ingredientTemplate) {
      addIngredient.addEventListener("click", function () {
        var fragment = ingredientTemplate.content.cloneNode(true);
        ingredientTable.appendChild(fragment);
        var rows = ingredientTable.querySelectorAll(".ingredient-row");
        var last = rows[rows.length - 1];
        var input = last && last.querySelector("input[name='ingredient_name']");
        if (input) input.focus();
      });
    }

    var stepList = document.getElementById("step-list");
    var addStep = document.getElementById("add-step");
    var stepTemplate = document.getElementById("step-template");
    function renumberSteps() {
      if (!stepList) return;
      stepList.querySelectorAll(".step-row").forEach(function (row, index) {
        var label = row.querySelector(".step-no");
        if (label) label.textContent = String(index + 1).padStart(2, "0");
      });
    }
    if (stepList && addStep && stepTemplate) {
      addStep.addEventListener("click", function () {
        var fragment = stepTemplate.content.cloneNode(true);
        stepList.appendChild(fragment);
        renumberSteps();
        var rows = stepList.querySelectorAll(".step-row");
        var last = rows[rows.length - 1];
        var area = last && last.querySelector("textarea");
        if (area) area.focus();
      });
    }

    form.addEventListener("click", function (event) {
      var button = event.target.closest(".remove-row");
      if (!button) return;
      var row = button.closest(".ingredient-row, .step-row");
      if (row) {
        row.remove();
        renumberSteps();
      }
    });

    var title = document.getElementById("f-title");
    var summary = document.getElementById("f-summary");
    var category = document.getElementById("f-category");
    var time = document.getElementById("f-time");
    var servings = document.getElementById("f-servings");
    var difficulty = document.getElementById("f-difficulty");
    var tags = document.getElementById("f-tags");
    var previewTitle = document.getElementById("preview-title");
    var previewSummary = document.getElementById("preview-summary");
    var previewCategory = document.getElementById("preview-category");
    var previewTime = document.getElementById("preview-time");
    var previewServings = document.getElementById("preview-servings");
    var previewDifficulty = document.getElementById("preview-difficulty");
    var previewTags = document.getElementById("preview-tags");

    function renderTags() {
      if (!previewTags || !tags) return;
      previewTags.innerHTML = "";
      (tags.value || "").split(/[,，、\s]+/).filter(Boolean).slice(0, 6).forEach(function (tag) {
        var node = document.createElement("span");
        node.textContent = tag;
        previewTags.appendChild(node);
      });
    }

    function renderText() {
      if (previewTitle && title) previewTitle.textContent = title.value.trim() || "菜名会显示在这里";
      if (previewSummary && summary) previewSummary.textContent = summary.value.trim() || "一句话介绍，告诉别人这道菜为什么值得做。";
      if (previewCategory && category) previewCategory.textContent = category.options[category.selectedIndex] ? category.options[category.selectedIndex].text : "";
      if (previewTime && time) previewTime.textContent = (time.value || "20") + " 分钟";
      if (previewServings && servings) previewServings.textContent = (servings.value || "2") + " 人份";
      if (previewDifficulty && difficulty) previewDifficulty.textContent = difficulty.value;
    }

    [title, summary, time, servings].forEach(function (node) {
      if (node) node.addEventListener("input", renderText);
    });
    [category, difficulty].forEach(function (node) {
      if (node) node.addEventListener("change", renderText);
    });
    if (tags) tags.addEventListener("input", renderTags);

    var coverInput = document.getElementById("f-cover");
    var coverPreview = document.getElementById("cover-preview");
    var previewCover = document.getElementById("preview-cover");
    var coverFile = document.getElementById("cover-file");
    var ratioBadge = document.querySelector(".cover-ratio");

    function coverSrc(value) {
      value = (value || "").trim();
      if (!value) return window.RECIPE_EDITOR.coverFallback;
      if (/^https?:\/\//.test(value) || value.charAt(0) === "/") return value;
      if (value.indexOf("uploads/") === 0) return "/" + value;
      return "/static/" + value;
    }

    function setCover(value) {
      var src = coverSrc(value);
      if (coverPreview) coverPreview.src = src;
      if (previewCover) previewCover.src = src;
    }

    if (coverInput) {
      var debounce;
      coverInput.addEventListener("input", function () {
        clearTimeout(debounce);
        debounce = setTimeout(function () { setCover(coverInput.value); }, 220);
      });
    }

    if (coverFile) {
      coverFile.addEventListener("change", function () {
        var file = coverFile.files && coverFile.files[0];
        if (!file) return;
        var reader = new FileReader();
        reader.onload = function () {
          if (coverPreview) coverPreview.src = reader.result;
          if (previewCover) previewCover.src = reader.result;
          var probe = new Image();
          probe.onload = function () {
            if (ratioBadge) {
              ratioBadge.textContent = probe.naturalWidth + "×" + probe.naturalHeight + " → 4:3";
            }
            toast("已选择封面，保存后自动裁成 1200×900");
          };
          probe.src = reader.result;
        };
        reader.readAsDataURL(file);
      });
    }

    renderText();
    renderTags();
  }

  document.addEventListener("DOMContentLoaded", function () {
    initNav();
    initConfirm();
    initAlerts();
    initEditor();
  });
})();
