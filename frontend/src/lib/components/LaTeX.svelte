<script>
  import { onMount } from 'svelte';
  import katex from 'katex';

  export let math = '';
  export let displayMode = false;
  export let className = '';

  let element;

  function renderMath() {
    if (element && math) {
      try {
        // Clean the LaTeX string - remove common formatting issues
        const cleanMath = math
          .replace(/\\mathrm\{([^}]+)\}/g, '\\text{$1}')  // Convert \mathrm to \text
          .replace(/\$([^$]+)\$/g, '$1')  // Remove dollar signs if present
          .trim();

        katex.render(cleanMath, element, {
          displayMode,
          throwOnError: false,
          errorColor: '#cc0000',
          strict: false,
          trust: false
        });
      } catch (error) {
        console.warn('KaTeX rendering error:', error);
        // Fallback to plain text if rendering fails
        element.textContent = math;
      }
    }
  }

  onMount(() => {
    renderMath();
  });

  // Re-render when math prop changes
  $: if (element && math) {
    renderMath();
  }
</script>

<span bind:this={element} class="latex-container {className}"></span>

<style>
  .latex-container {
    display: inline-block;
  }
  
  /* Ensure KaTeX math matches surrounding text color in dark mode */
  :global(.dark .latex-container .katex) {
    color: inherit;
  }
  
  :global(.latex-container .katex .mord) {
    color: inherit;
  }
</style>