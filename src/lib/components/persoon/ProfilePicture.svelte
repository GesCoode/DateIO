<script lang="ts">
    import LabeledInput from "$lib/components/form/LabeledInput.svelte";
    import SimpleButton from "$lib/components/form/SimpleButton.svelte";
    import LabeledSliderInfo from "$lib/components/composits/LabeledSliderInfo.svelte";
    import TempImage from "$lib/assets/EmptyProfilePicture3.png";

    export let fotoZichtbaarheid: boolean = false;

    // **Profile image state**
    let profileImage: string = TempImage;

    // Handle file selection
    function handleFileChange(event: Event) {
        const target = event.target as HTMLInputElement;
        if (target.files && target.files.length > 0) {
            const file = target.files[0];

            // Limit file size to 2MB
            if (file.size > 2 * 1024 * 1024) {
                alert("Bestand is te groot. Maximaal 2MB.");
                return;
            }

            const reader = new FileReader();
            reader.onload = () => {
                profileImage = reader.result as string;
            };
            reader.readAsDataURL(file);
        }
    }

    // Trigger the hidden file input
    let fileInput: HTMLInputElement;
    function openFilePicker() {
        fileInput.click();
    }
</script>

<!-- Profile picture -->
<div class="flex flex-col items-center gap-4 px-4 py-6">
    <div
        class="w-[160px] h-[160px] rounded-[60px] overflow-hidden border-2 border-gray-300"
    >
        <img
            src={profileImage}
            alt="Profile"
            class="w-full h-full object-cover"
        />
    </div>

    <div class="flex flex-col items-center items-start gap-2">
        <SimpleButton
            text="Nieuwe foto"
            bgColor="#0C3986"
            textColor="#FFF"
            onClick={openFilePicker}
        />

        <!-- Hidden file input -->
        <input
            type="file"
            accept="image/*"
            bind:this={fileInput}
            on:change={handleFileChange}
            class="hidden"
        />
    </div>

    <LabeledSliderInfo
        label="Foto zichtbaarheid"
        tooltipText=""
        statusTextTrue="Foto is zichtbaar"
        statusTextFalse="Foto is niet zichtbaar"
        bind:checked={fotoZichtbaarheid}
        handleColor="#FFF"
        trueColor="#45B652"
        statusTextColor="#374151"
        showTooltip={false}
    />
</div>
