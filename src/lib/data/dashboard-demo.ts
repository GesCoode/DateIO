export type ModelStatus = 'ready' | 'training' | 'needs_photos';

export type Generation = {
	id: string;
	scene: string;
	prompt: string;
	hue: number;
	favorite: boolean;
	createdAt: string;
};

export const demoUser = {
	name: 'Alex',
	email: 'alex@example.com',
	tokens: 24,
	modelStatus: 'ready' as ModelStatus,
	modelLabel: 'Personal LoRA v1',
	referenceCount: 12,
	trainingProgress: null as number | null
};

export const recentGenerations: Generation[] = [
	{
		id: 'g1',
		scene: 'Café window',
		prompt: 'Warm smile, café candid, soft window light',
		hue: 145,
		favorite: true,
		createdAt: '2 hours ago'
	},
	{
		id: 'g2',
		scene: 'Rooftop sunset',
		prompt: 'Golden hour, relaxed posture, city skyline',
		hue: 95,
		favorite: false,
		createdAt: '2 hours ago'
	},
	{
		id: 'g3',
		scene: 'Park path',
		prompt: 'Outdoor portrait, natural greenery, casual outfit',
		hue: 125,
		favorite: true,
		createdAt: 'Yesterday'
	},
	{
		id: 'g4',
		scene: 'Bookshop',
		prompt: 'Thoughtful look, indoor ambient, date-night energy',
		hue: 160,
		favorite: false,
		createdAt: 'Yesterday'
	},
	{
		id: 'g5',
		scene: 'City night',
		prompt: 'Evening street lights, confident smile',
		hue: 175,
		favorite: false,
		createdAt: '3 days ago'
	},
	{
		id: 'g6',
		scene: 'Wine bar',
		prompt: 'Candid laugh, warm interior tones',
		hue: 135,
		favorite: true,
		createdAt: '3 days ago'
	}
];
