<script>
	import { isLogged, load_page_index } from './get_stores'
	import { is_logged, page_index } from './stores';
	import './static/loginstyle.css';

	let user = "GUEST";
	let email;
	let secretKey;

	function submit_form()
	{
		const data = fetch(`http://localhost:${EXPRESS_PORT}/login`, {
			method: "POST",
			body: JSON.stringify({
				email: email,
				password: secretKey
			}),
			headers: {
				"Content-Type": "application/json",
				'Access-Control-Allow-Headers':
					'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
				'Access-Control-Allow-Methods': 'OPTIONS,POST',
				'Access-Control-Allow-Credentials': true,
				'Access-Control-Allow-Origin': '*',
				'X-Requested-With': '*',
			}
		}).then(data => data.json())
		  .then(response => console.log("Success:", response))
		  .catch(err => console.error(err))


		let user = data.username;
		is_logged.set(true)
		page_index.set(1)
		window.alert('Giris Basarili')
		window.alert(user)
	}
	$: logged = isLogged();
	$: ui = load_page_index()
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
        <br>
        <form on:submit|preventDefault={submit_form} method="POST" name="loginform" onsubmit="return false" autocomplete="off">
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
			<u>Şikayet Değerlendirme:</u>
		</h1>
	</center>
</main>
{:else}
<center>404 Error: Page Not Found!</center>
{/if}

<style>
	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>
