<script>
	import { isLogged, load_page_index } from './get_stores.mjs'
	import { is_logged, page_index, user_data } from './stores.mjs';
	import './static/loginstyle.css';

	let username = "GUEST";
	let email;
	let secretKey;
	let complaints = [];

	// for frotend
	let zero_to_n = [];
	let br_limit = 12
	for(let i = 0; i <= br_limit; i++)
	{
		zero_to_n.push(i)
	}

	async function process_complaint_case_data(comp_id)
	{
		// EXPRESS_PORT IS DEFINED IN rollup.config.js
		const data = await fetch(`http://localhost:${EXPRESS_PORT}/complaint_case`, {
			method: "POST",
			body: JSON.stringify({
				comp_id: comp_id
			}),
			headers: {
				"Content-Type": "application/json",
				'Access-Control-Allow-Methods': 'OPTIONS,POST',
				'Access-Control-Allow-Credentials': true,
				'Access-Control-Allow-Origin': '*',
				'X-Requested-With': '*',
			}
		})

		const response = await data.json();

		if(response.status === 200)
		{
			return response.data;
		}
	}

	async function submit_form(email, secretKey)
	{
		// EXPRESS_PORT IS DEFINED IN rollup.config.js
		const data = await fetch(`http://localhost:${EXPRESS_PORT}/login`, {
			method: "POST",
			body: JSON.stringify({
				email: email,
				secretKey: secretKey
			}),
			headers: {
			"Content-Type": "application/json",
			'Access-Control-Allow-Methods': 'OPTIONS,POST',
			'Access-Control-Allow-Credentials': true,
			'Access-Control-Allow-Origin': '*',
			'X-Requested-With': '*',
			}
		})
		const result = await data.json()

		if (result.response === 200)
		{
			// set stores!
			user_data.set(result.user_data);
			is_logged.set(true)
			page_index.set(1)
			// set variables
			username = result.user_data.username;
			logged = true;
			ui = 1;
			window.alert(`Hoşgeldiniz, ${username}!\nSisteme erişim veriliyor...`)
		} else if(result.response === 403){
			window.alert('ADMIN OLMADIĞINIZ HALDE SİSTEME ERİŞİM\nSAĞLAMAYA ÇALIŞTIĞINIZDAN BANLANIYORSUNUZ.')
			setTimeout(() => window.close(), 2000)
		} else {
			window.alert('GİRİŞ BAŞARISIZ!!!')
		}
	}

	async function get_complaints(email, secretKey)
		{
		// EXPRESS_PORT IS DEFINED IN rollup.config.js
		const data = await fetch(`http://localhost:${EXPRESS_PORT}/login`, {
			method: "POST",
			body: JSON.stringify({
				email: email,
				secretKey: secretKey
			}),
			headers: {
			"Content-Type": "application/json",
			'Access-Control-Allow-Methods': 'OPTIONS,POST',
			'Access-Control-Allow-Credentials': true,
			'Access-Control-Allow-Origin': '*',
			'X-Requested-With': '*',
			}
		});

		const result = await data.json();

		if (result.response === 200)
		{
			return result.data
		} else {
			return "ERROR_CANNOT_GET_COMPLAINTS";
		}
	}

	const send_form = () => {
		submit_form(email, secretKey);
		complaints = get_complaints(email, secretKey)
	}

	// reactives
	let logged_reactive_component = isLogged();
	let logged = logged_reactive_component ?? false;

	let ui_reactive_component = load_page_index();
	let ui = ui_reactive_component ?? 0;

	let title_list = ["Giriş Sayfası", "Ana Sayfa / Şikaye Değerlendirme"];
	$: title_reactive = title_list[ui]
</script>
<svelte:head>
	<title>GaServer Desktop Client | {title_reactive ?? "Ana Sayfa"}</title>
</svelte:head>
{#if ui === 0}
<main>
    <div class="login-box">
        <h2>Admin Panel Giriş Formu</h2>
        <br/>
        <form on:submit|preventDefault={send_form} method="POST" name="loginform" autocomplete="off">
            <div class="user-box">
                <input bind:value={email} type="email" name="email" placeholder="Kullanıcı E-mail" required="">
            </div>
            <div class="user-box">
                <input bind:value={secretKey} type="password" name="password" placeholder="Günlük değişen gizli anahtar..." required="">
            </div>
            <!-- svelte-ignore a11y-invalid-attribute -->
            <a href="#">
                <span></span>
                <span></span>
                <span></span>
                <span></span>
                <input type="submit" value="Giriş yap!"/>
            </a>
        </form>
    </div>
</main>
{:else if ui === 1 && logged}
<main>
	<center>
		<h1>
			<u class="text-white my-2" style="font-family:monospace; font-size: 2.5rem; color: white;">Şikayet Değerlendirme:</u>
		</h1>
		{#each complaints as complaint}
			Sikayet: {complaint}
		{/each}
	</center>
</main>
{:else}
{#each zero_to_n as i}
	<br/>
{/each}
<center style="font-family: monospace !important; font-size: 3rem; display:flex; justify-content:center; align-items:center; color:white;">
	404 Hatası: Sayfa Bulunamadı!
</center>
{/if}

<style>
	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>
