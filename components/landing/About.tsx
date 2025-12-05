'use client'

import { Card, CardContent } from '@/components/ui/card'
import { Sparkles, TrendingUp } from 'lucide-react'

export default function About() {
  return (
    <section className="py-20 sm:py-32">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-4xl text-center mb-16">
          <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl lg:text-5xl mb-4">
            Built by Founders, for Founders
          </h2>
          <p className="text-lg text-muted-foreground sm:text-xl">
            We've been in your shoes. Now we're making investor matching accessible to every founder.
          </p>
        </div>
        
        <div className="grid grid-cols-1 gap-8 lg:grid-cols-2 max-w-5xl mx-auto">
          <Card className="border-2">
            <CardContent className="p-8">
              <div className="flex items-start gap-6">
                <div className="flex h-16 w-16 shrink-0 items-center justify-center rounded-full bg-primary/10">
                  <Sparkles className="h-8 w-8 text-primary" />
                </div>
                <div className="flex-1">
                  <h3 className="text-2xl font-bold mb-2">AI-Powered Matching</h3>
                  <p className="text-muted-foreground leading-7 mb-4">
                    Our advanced AI analyzes thousands of investors to find the perfect matches for your startup. 
                    We understand what investors care about and match you based on industry, stage, geography, and investment focus.
                  </p>
                  <p className="text-sm font-medium text-primary">
                    "Making investor discovery accessible to every founder."
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card className="border-2">
            <CardContent className="p-8">
              <div className="flex items-start gap-6">
                <div className="flex h-16 w-16 shrink-0 items-center justify-center rounded-full bg-primary/10">
                  <TrendingUp className="h-8 w-8 text-primary" />
                </div>
                <div className="flex-1">
                  <h3 className="text-2xl font-bold mb-2">Proven Results</h3>
                  <p className="text-muted-foreground leading-7 mb-4">
                    We've analyzed hundreds of pitch decks and matched startups with relevant investors. 
                    Our platform uses semantic search and AI to understand your business and find investors who actually invest in your space.
                  </p>
                  <p className="text-sm font-medium text-primary">
                    "Hacked the hardest part of fundraising – finding the right investors."
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  )
}
