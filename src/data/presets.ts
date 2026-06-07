import type { ResearchPreset } from '../lib/types'

export const RESEARCH_PRESETS: ResearchPreset[] = [
    {
        id: 'ev-policy',
        title: 'EV Policy Analysis',
        description: 'Analyze electric vehicle policy impacts on automotive industry',
        query: "Analyze Indonesia's 2026 electric vehicle policy and its impact on the automotive industry, including market trends, consumer adoption, and manufacturing changes.",
        category: 'business',
        icon: 'Car',
    },
    {
        id: 'ai-market',
        title: 'AI Market Research',
        description: 'Comprehensive AI market analysis with trends and forecasts',
        query: 'Conduct a comprehensive market analysis of the artificial intelligence industry in Southeast Asia, including key players, investment trends, and growth projections for 2026-2030.',
        category: 'business',
        icon: 'Brain',
    },
    {
        id: 'climate-tech',
        title: 'Climate Tech Innovation',
        description: 'Research emerging climate technologies and solutions',
        query: 'Research the latest innovations in climate technology, focusing on carbon capture, renewable energy storage, and sustainable agriculture solutions being developed globally.',
        category: 'technical',
        icon: 'Leaf',
    },
    {
        id: 'fintech-regulation',
        title: 'Fintech Regulations',
        description: 'Analyze fintech regulatory landscape',
        query: 'Analyze the current regulatory landscape for fintech companies in Indonesia, including digital banking, cryptocurrency, and payment systems regulations.',
        category: 'business',
        icon: 'Landmark',
    },
    {
        id: 'quantum-computing',
        title: 'Quantum Computing',
        description: 'Latest developments in quantum computing research',
        query: 'Provide an overview of the latest developments in quantum computing, including recent breakthroughs, commercial applications, and key research institutions.',
        category: 'academic',
        icon: 'Atom',
    },
    {
        id: 'healthcare-ai',
        title: 'AI in Healthcare',
        description: 'AI applications transforming healthcare delivery',
        query: 'Research how artificial intelligence is being applied in healthcare, including diagnostic tools, drug discovery, patient care optimization, and ethical considerations.',
        category: 'technical',
        icon: 'HeartPulse',
    },
    {
        id: 'cybersecurity',
        title: 'Cybersecurity Trends',
        description: 'Emerging cybersecurity threats and solutions',
        query: 'Analyze emerging cybersecurity threats for 2026, including AI-powered attacks, ransomware evolution, and enterprise security solutions.',
        category: 'technical',
        icon: 'Shield',
    },
    {
        id: 'sustainable-fashion',
        title: 'Sustainable Fashion',
        description: 'Sustainability trends in fashion industry',
        query: 'Investigate the sustainable fashion movement, including circular economy practices, eco-friendly materials, and consumer behavior shifts toward ethical fashion.',
        category: 'general',
        icon: 'Shirt',
    },
]

export function getPresetsByCategory(category: ResearchPreset['category']) {
    return RESEARCH_PRESETS.filter(preset => preset.category === category)
}

export function getPresetById(id: string) {
    return RESEARCH_PRESETS.find(preset => preset.id === id)
}

