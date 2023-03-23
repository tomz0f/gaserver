<script>
	import { isLogged, load_page_index } from './get_stores'
	import { is_logged, page_index, user_data } from './stores';
	import { submit_form, get_complaints } from './api';
	import './static/loginstyle.css';

	let username = "GUEST";
	let email;
	let secretKey;

	// for frotend
	let zero_to_n = [];
	let br_limit = 12
	for(let i = 0; i <= br_limit; i++)
	{
		zero_to_n.push(i)
	}

	const send_form = () => submit_form(email, secretKey);
	const get_compt = () => get_complaints(email, secretKey);

	// reactives
	let logged_reactive_component = isLogged();
	let logged = true;
	// let logged = logged_reactive_component ?? false;

	let ui_reactive_component = load_page_index();
	let ui = 1;
	//let ui = ui_reactive_component ?? 0;

	let title_list = ["Ana Sayfa", "Giriş Sayfası", "Admin Panel"];
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
			<u class="text-white my-2" style="color: white;">Şikayet Değerlendirme:</u>
		</h1>
	</center>
</main>
{:else}
{#each zero_to_n as i}
	<br/>
{/each}
<center style="font-size: 3rem; display:flex; justify-content:center; align-items:center; color:white;">
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
