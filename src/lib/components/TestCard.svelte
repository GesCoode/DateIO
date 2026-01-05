<script lang="ts">
  export let title: string;
</script>

<div class="rounded-xl border p-12 shadow-sm bg-yellow">
  <h2 class="text-xl font-semibold">{title}</h2>
  <slot />
</div>
