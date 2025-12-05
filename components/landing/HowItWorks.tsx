'use client'

import { Card, CardContent } from '@/components/ui/card'
import { Upload, Sparkles, MessageSquare, Mail } from 'lucide-react'

const steps = [
  {
    number: '01',
    icon: Upload,
    title: 'Upload Your Pitch Deck',
    description: 'Drag and drop your PDF pitch deck or browse to upload. Our system will extract all relevant information automatically.',
  },
  {
    number: '02',
    icon: Sparkles,
    title: 'AI Analysis',
    description: 'Advanced AI analyzes your business model, industry, stage, funding needs, and key differentiators.',
  },
  {
    number: '03',
    icon: MessageSquare,
    title: 'Ask Questions',
    description: 'Refine your search by asking specific questions. Find investors by location, check size, or focus area.',
  },
  {
    number: '04',
    icon: Mail,
    title: 'Get Matches & Connect',
    description: 'Receive ranked investor recommendations with detailed explanations and direct contact information.',
  },
]

export default function HowItWorks() {
  return (
    <section id="how-it-works" className="py-20 sm:py-32">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-2xl text-center mb-16">
          <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
            How It Works
          </h2>
          <p className="mt-4 text-lg text-muted-foreground">
            Get from pitch deck to investor introductions in four simple steps.
          </p>
        </div>
        
        <div className="relative">
          <div className="absolute left-1/2 top-0 h-full w-0.5 -translate-x-1/2 bg-border hidden lg:block" />
          
          <div className="grid grid-cols-1 gap-8 lg:grid-cols-2 lg:gap-12">
            {steps.map((step, index) => {
              const Icon = step.icon
              const isEven = index % 2 === 1
              
              return (
                <div
                  key={step.number}
                  className={`relative flex items-start gap-6 ${
                    isEven ? 'lg:mt-20 lg:flex-row-reverse' : ''
                  }`}
                >
                  <div className={`flex-1 ${isEven ? 'lg:text-right' : ''}`}>
                    <Card className="border-2">
                      <CardContent className="p-6">
                        <div className={`flex items-center gap-4 ${isEven ? 'lg:flex-row-reverse' : ''}`}>
                          <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-primary text-primary-foreground text-lg font-bold">
                            {step.number}
                          </div>
                          <div className="flex-1">
                            <div className={`mb-2 flex items-center gap-2 ${isEven ? 'lg:justify-end' : ''}`}>
                              <Icon className="h-5 w-5 text-primary" />
                              <h3 className="text-xl font-semibold">{step.title}</h3>
                            </div>
                            <p className="text-muted-foreground">
                              {step.description}
                            </p>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      </div>
    </section>
  )
}

