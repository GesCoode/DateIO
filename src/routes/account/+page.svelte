<script lang="ts">
    import LeftAccountBlock from "$lib/components/account/LeftAccountBlock.svelte";
    import RightAccountBlock from "$lib/components/account/RightAccountBlock.svelte";
    import accountImage from "$lib/assets/TempImage1.png";

    let nieuwWachtwoord = "";
    let herhaalNieuwWachtwoord = "";
    let deactiveerAccount = false;

    let newsletterEnabled = true;
    let gegevensWaarschuwingEnabled = false;
    const email = "example@gmail.com";

    function handleChangePassword() {
        alert("Button clicked!");
    }

    function handleVerwijderAccount() {
        alert("Account verwijderd");
    }
</script>

<div class="w-full px-5 flex flex-col items-start">
    <div class="flex flex-col lg:flex-row gap-3 self-stretch">
        <!-- Left block -->
        <div class="h-[600px] w-full lg:flex-1 flex flex-col gap-3">
            <LeftAccountBlock
                bind:nieuwWachtwoord
                bind:herhaalNieuwWachtwoord
                bind:deactiveerAccount
                {handleChangePassword}
                {handleVerwijderAccount}
            />
        </div>

        <!-- Right block -->
        <div class="h-[600px] w-full lg:flex-1 flex flex-col gap-3">
            <RightAccountBlock
                {email}
                bind:newsletterEnabled
                bind:gegevensWaarschuwingEnabled
            />
        </div>

        <!-- Image -->
        <img
            src={accountImage}
            alt="Gezellige eettafel"
            class="hidden lg:block h-[600px] w-[360px] object-cover flex-shrink-0"
        />
    </div>
</div>
