<script>
	let ui = 0
	let title_list = ["Ana Sayfa", "Giriş Sayfası", "Admin Panel"];

	$: ui_reactive = title_list[ui]
</script>
<svelte:head>
	<title>GaServer Desktop Client | {ui_reactive ?? "Ana Sayfa"}</title>
</svelte:head>

{#if ui === 0}
<main>
	<h1>Hello!</h1>
	<p>Visit the <a href="https://svelte.dev/tutorial">Svelte tutorial</a> to learn how to build Svelte apps.</p>
</main>
{:else if ui === 1}

{:else}
<center>404 ERROR!!!</center>
{/if}
<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>