<script lang="ts">
    import SimpleButton from "$lib/components/form/SimpleButton.svelte";
    import DropdownButton from "../form/DropdownButton.svelte";
    import BlinkingButton from "./BlinkingButton.svelte";

    function SetAbo(id: string) {
        verlengen = id;
    }

    export let verlengen: string = "none";
    export let handleVerlengen: () => void = () => {};
</script>

<div class="flex h-full flex-1 justify-center items-center bg-[#0C3966]">
    <div class="flex flex-col items-center gap-6 w-full">
        <div class="text-white font-spaceGrotesk text-[20px] font-bold">
            Mijn abonnement
        </div>

        <!-- Abonnement informatie -->
        <div
            class="flex flex-col md:flex-row xl:flex-col 2xl:flex-row gap-4 px-4 w-full"
        >
            <!-- Block 1: Startdatum + Einddatum -->
            <div class="flex flex-row flex-1 gap-4">
                <!-- Startdatum -->
                <div class="flex flex-1 flex-col items-center gap-4">
                    <div
                        class="text-white font-spaceGrotesk text-[14px] font-medium text-center"
                    >
                        Startdatum
                    </div>
                    <div
                        class="text-white font-spaceGrotesk text-[16px] font-bold tracking"
                    >
                        01-01-2026
                    </div>
                </div>

                <!-- Einddatum -->
                <div class="flex flex-1 flex-col items-center gap-4">
                    <div
                        class="text-white font-spaceGrotesk text-[14px] font-medium text-center"
                    >
                        Einddatum
                    </div>
                    <div
                        class="text-white font-spaceGrotesk text-[16px] font-bold tracking"
                    >
                        01-01-2027
                    </div>
                </div>
            </div>

            <!-- Block 2: Dagen resterend + Soort abonnement -->
            <div class="flex flex-row flex-1 gap-4">
                <!-- Dagen resterend -->
                <div class="flex flex-1 flex-col items-center gap-4">
                    <div
                        class="text-white font-spaceGrotesk text-[14px] font-medium text-center"
                    >
                        Dagen resterend
                    </div>
                    <div
                        class="text-white font-spaceGrotesk text-[16px] font-bold tracking text-center"
                    >
                        362
                    </div>
                </div>

                <!-- Soort abonnement -->
                <div class="flex flex-1 flex-col items-center gap-4">
                    <div
                        class="text-white font-spaceGrotesk text-[14px] font-medium text-center"
                    >
                        Soort abonnement
                    </div>
                    <div
                        class="text-white font-spaceGrotesk text-[16px] font-bold tracking"
                    >
                        1 Jaar
                    </div>
                </div>
            </div>
        </div>

        <div class="flex flex-col gap-2 items-center">
            <!-- Verlengen -->
            <div class="text-white font-spaceGrotesk text-[20px] font-bold">
                Verlengen
            </div>

            <DropdownButton
                label="Selecteer duur"
                buttonBg="#FFF"
                buttonText="#0C3966"
                dropdownBg="#FFF"
                dropdownBorder="#D1D5DB"
                items={[
                    { label: "1 jaar", onClick: () => SetAbo("1") },
                    { label: "2 jaar", onClick: () => SetAbo("2") },
                    { label: "3 jaar", onClick: () => SetAbo("3") },
                ]}
            />

            <BlinkingButton
                text="Verleng mijn abonnement"
                bgColor="#FFF"
                textColor="#0C3966"
                activated={verlengen !== "none"}
                onClick={handleVerlengen}
            />
        </div>

        <div class="flex flex-col items-start"></div>
    </div>
</div>
