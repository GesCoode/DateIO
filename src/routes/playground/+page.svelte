<script lang="ts">
	import LabeledInput from "$lib/components/form/LabeledInput.svelte";
	import SliderButton from "$lib/components/form/SliderButton.svelte";
	import InfoTooltip from "$lib/components/form/InfoTooltip.svelte";
	import LabeledSliderInfo from "$lib/components/composits/LabeledSliderInfo.svelte";
	import ContactPersoon from "$lib/components/medisch/ContactPersoon.svelte";
	import InformationBox from "$lib/components/form/InformationBox.svelte";
	import BewerkPopUp from "$lib/components/soscodes/editPopUp.svelte";

	let username = "";

	let isEnabled = false;
	function handleToggle(value: boolean) {
		isEnabled = value;
		console.log("Slider is now:", isEnabled);
	}

	let newsletterEnabled: boolean = true;
</script>

<section class="p-8 space-y-6 max-w-md">
	<h1 class="text-3xl font-bold">Playground</h1>

	<LabeledInput
		id="username"
		label="Username"
		placeholder="Enter your username"
		bind:value={username}
		tooltipText="We will only use your email for updates"
		showTooltip={true}
	/>

	<p class="text-sm text-gray-600">
		Current value: <strong>{username}</strong>
	</p>
</section>

<SliderButton
	checked={isEnabled}
	onChange={(v) => (isEnabled = v)}
	handleColor="#FFD700"
	trueColor="#0CFF66"
	ariaLabel="Enable feature"
/>

<InfoTooltip infoText="This is some helpful information for the user." />

<LabeledSliderInfo
	label="Receive newsletter"
	tooltipText="If enabled, you will receive our newsletter via email."
	statusTextTrue="You currently receive the newsletter"
	statusTextFalse="You currently do NOT receive the newsletter"
	checked={newsletterEnabled}
	onChange={(v) => (newsletterEnabled = v)}
	handleColor="#FFF"
	trueColor="#FF0000"
/>

<ContactPersoon></ContactPersoon>

<InformationBox>
	<p>Eerste regel</p>
	<p>Tweede regel</p>
	<p>Derde regel</p>
</InformationBox>

<BewerkPopUp></BewerkPopUp>
