Component({
  properties: {
    recipe: { type: Object, value: {} },
    variant: { type: String, value: "row" },
  },
  methods: {
    onTap() {
      this.triggerEvent("select", { id: this.data.recipe.id });
    },
  },
});
