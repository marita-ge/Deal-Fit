'use client'

import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { ArrowRight, Sparkles } from 'lucide-react'

export default function Hero() {
  return (
    <section className="relative overflow-hidden bg-gradient-to-b from-background to-muted/20 py-20 sm:py-32">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-3xl text-center">
          <div className="mb-8 flex justify-center">
            <div className="relative rounded-full bg-primary/10 px-4 py-1.5 text-sm font-medium text-primary">
              <Sparkles className="mr-2 inline h-4 w-4" />
              AI-Powered Investor Matching
            </div>
          </div>
          
          <h1 className="text-4xl font-bold tracking-tight text-foreground sm:text-6xl lg:text-7xl">
            Find Your Perfect
            <span className="block text-primary">Investor Match</span>
          </h1>
          
          <p className="mt-6 text-lg leading-8 text-muted-foreground sm:text-xl">
            Upload your pitch deck and let AI analyze it to find the most relevant investors
            for your startup. Get personalized recommendations with direct contact information.
          </p>
          
          <div className="mt-10 flex items-center justify-center gap-x-6">
            <Link href="/chat">
              <Button size="lg" className="group">
                Get Started
                <ArrowRight className="ml-2 h-4 w-4 transition-transform group-hover:translate-x-1" />
              </Button>
            </Link>
            <Link href="#how-it-works">
              <Button variant="outline" size="lg">
                Learn More
              </Button>
            </Link>
          </div>
          
          <div className="mt-16 flex items-center justify-center gap-8 text-sm text-muted-foreground">
            <div className="text-center">
              <div className="text-2xl font-bold text-foreground">725+</div>
              <div>Investors</div>
            </div>
            <div className="h-12 w-px bg-border" />
            <div className="text-center">
              <div className="text-2xl font-bold text-foreground">AI-Powered</div>
              <div>Matching</div>
            </div>
            <div className="h-12 w-px bg-border" />
            <div className="text-center">
              <div className="text-2xl font-bold text-foreground">Direct</div>
              <div>Contacts</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
