'use client'

import { Card, CardContent } from '@/components/ui/card'
import { Brain, Target, Zap } from 'lucide-react'

export default function About() {
  return (
    <section className="py-20 sm:py-32 bg-muted/30">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-3xl text-center mb-16">
          <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl mb-4">
            Why Deal Fit Works
          </h2>
          <p className="text-lg text-muted-foreground">
            We use advanced AI to understand your business and match you with investors who actually invest in your space.
          </p>
        </div>
        
        <div className="grid grid-cols-1 gap-6 md:grid-cols-3 max-w-6xl mx-auto">
          <Card className="border-2 hover:border-primary/50 transition-colors">
            <CardContent className="p-6">
              <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10 mb-4">
                <Brain className="h-6 w-6 text-primary" />
              </div>
              <h3 className="text-xl font-bold mb-2">Smart Analysis</h3>
              <p className="text-muted-foreground leading-6">
                Our AI reads your pitch deck and understands your business model, market, and funding needs.
              </p>
            </CardContent>
          </Card>
          
          <Card className="border-2 hover:border-primary/50 transition-colors">
            <CardContent className="p-6">
              <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10 mb-4">
                <Target className="h-6 w-6 text-primary" />
              </div>
              <h3 className="text-xl font-bold mb-2">Precise Matching</h3>
              <p className="text-muted-foreground leading-6">
                We match you based on industry focus, investment stage, check size, and geographic preferences.
              </p>
            </CardContent>
          </Card>
          
          <Card className="border-2 hover:border-primary/50 transition-colors">
            <CardContent className="p-6">
              <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10 mb-4">
                <Zap className="h-6 w-6 text-primary" />
              </div>
              <h3 className="text-xl font-bold mb-2">Instant Results</h3>
              <p className="text-muted-foreground leading-6">
                Get ranked recommendations with explanations and direct contact information in minutes.
              </p>
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  )
}
