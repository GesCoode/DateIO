export type FaqItem = {
	id: string;
	question: string;
	answer: string;
};

export const faqItems: FaqItem[] = [
	{
		id: 'how-studio-model-works',
		question: 'How does the Visagely Studio Model work under the hood?',
		answer:
			'Visagely builds a personalized AI model trained on your uploaded photos. It learns your facial structure, expressions, and visual characteristics, then uses a multi-stage image generation pipeline to create new, realistic photos that stay consistent with your identity while allowing different styles, settings, and moods.'
	},
	{
		id: 'look-like-me-or-ai',
		question: 'Will the photos actually look like me or like AI?',
		answer:
			'They are designed to look like you. The system is trained to preserve your facial identity and natural features while generating new high-quality photos. The goal is realism, not an AI-generated look.'
	},
	{
		id: 'exaggerate-attractiveness',
		question: 'Do you exaggerate attractiveness or change features?',
		answer:
			'No. Visagely does not alter your identity or reconstruct your face. It generates new photos based on your existing features, optimized for lighting, composition, and style so you look your best in realistic dating scenarios.'
	},
	{
		id: 'face-train-other-models',
		question: 'Is my face used to train other people’s models?',
		answer:
			'No. Your data is used only to create your personal model and is never used to train models for other users.'
	},
	{
		id: 'delete-data-model',
		question: 'Can I delete my data and model?',
		answer:
			'Yes. You can request deletion of your uploaded photos and your trained model at any time.'
	},
	{
		id: 'more-matches',
		question: 'Will this actually get me more matches?',
		answer:
			'Better photos are one of the most important factors in online dating success. Visagely helps you present yourself clearly and attractively with high-quality images designed for dating apps, which can improve your chances of getting more matches.'
	},
	{
		id: 'vs-photographer',
		question: 'Why not just use a photographer?',
		answer:
			'Photography sessions can be expensive, time-consuming, and inconsistent. With Visagely, you can generate multiple high-quality dating photos in different styles without scheduling shoots or retakes. It is a faster and more flexible way to explore how you present yourself.'
	},
	{
		id: 'how-many-photos',
		question: 'How many photos do I need to upload?',
		answer:
			'You can get good results with around five photos. More variety helps improve accuracy and consistency of your personal model.'
	},
	{
		id: 'editing-skills-prompts',
		question: 'Do I need editing skills or prompts?',
		answer:
			'No. You can simply choose a vibe or describe what you want. Visagely handles the rest. You can still refine results if you want more control.'
	},
	{
		id: 'complicated-to-use',
		question: 'Is it complicated to use?',
		answer:
			'No. Upload a few photos, start training your model, and then generate images with simple prompts or presets once it is ready.'
	},
	{
		id: 'choose-how-i-look',
		question: 'Can I choose how I look in the photos?',
		answer:
			'Yes, within limits that preserve your identity. You can influence style, setting, clothing vibe, and mood while keeping your core appearance consistent.'
	},
	{
		id: 'guide-style-vibe',
		question: 'Can I guide the style or vibe?',
		answer:
			'Yes. You can fully control the style direction, from casual everyday shots to more polished or creative dating profile looks.'
	},
	{
		id: 'catfishing',
		question: 'Is it catfishing?',
		answer:
			'No. The images are generated from your own face and are designed to represent you realistically across different scenarios and lighting conditions.'
	},
	{
		id: 'allowed-on-dating-apps',
		question: 'Is it allowed on Tinder or Hinge?',
		answer:
			'Yes. The photos are based on your own identity and are intended to represent you in realistic dating profile contexts and can be used on major dating platforms.'
	}
];
