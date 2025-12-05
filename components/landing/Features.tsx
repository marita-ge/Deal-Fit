'use client'

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Upload, Search, Users, Zap } from 'lucide-react'

const features = [
  {
    icon: Upload,
    title: 'Upload Pitch Deck',
    description: 'Simply upload your PDF pitch deck. Our AI extracts and analyzes all key information automatically.',
  },
  {
    icon: Search,
    title: 'AI-Powered Search',
    description: 'Advanced semantic search matches your startup with investors based on industry, stage, and focus areas.',
  },
  {
    icon: Users,
    title: 'Smart Matching',
    description: 'Get ranked recommendations with detailed explanations of why each investor is a perfect fit.',
  },
  {
    icon: Zap,
    title: 'Direct Contacts',
    description: 'Access direct contact information for decision-makers, including emails and roles.',
  },
]

export default function Features() {
  return (
    <section id="features" className="py-20 sm:py-32 bg-muted/30">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-2xl text-center mb-16">
          <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
            Everything You Need
          </h2>
          <p className="mt-4 text-lg text-muted-foreground">
            A complete platform to find, analyze, and connect with the right investors for your startup.
          </p>
        </div>
        
        <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-4">
          {features.map((feature) => {
            const Icon = feature.icon
            return (
              <Card key={feature.title} className="border-2 hover:border-primary/50 transition-colors">
                <CardHeader>
                  <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10">
                    <Icon className="h-6 w-6 text-primary" />
                  </div>
                  <CardTitle className="text-xl">{feature.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-base">
                    {feature.description}
                  </CardDescription>
                </CardContent>
              </Card>
            )
          })}
        </div>
      </div>
    </section>
  )
}
