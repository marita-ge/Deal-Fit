'use client'

import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { ArrowRight, Sparkles } from 'lucide-react'

export default function Hero() {
  return (
    <section className="relative overflow-hidden bg-gradient-to-b from-background via-background to-muted/30 py-20 sm:py-28 lg:py-36">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-4xl text-center">
          <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-primary/20 bg-primary/5 px-4 py-2 text-sm font-medium text-primary">
            <Sparkles className="h-4 w-4" />
            AI-Powered Investor Discovery
          </div>
          
          <h1 className="text-5xl font-bold tracking-tight text-foreground sm:text-6xl lg:text-7xl">
            Stop Cold Emailing.
            <span className="block mt-2 bg-gradient-to-r from-primary to-primary/60 bg-clip-text text-transparent">
              Start Smart Matching.
            </span>
          </h1>
          
          <p className="mt-8 text-xl leading-8 text-muted-foreground sm:text-2xl max-w-2xl mx-auto">
            Upload your pitch deck and let AI find the perfect investors for your startup. 
            Get personalized recommendations with direct contact information in minutes.
          </p>
          
          <div className="mt-12 flex flex-col items-center justify-center gap-4 sm:flex-row">
            <Link href="/chat">
              <Button size="lg" className="group h-12 px-8 text-base font-semibold bg-primary text-primary-foreground hover:bg-primary/90 shadow-lg shadow-primary/25">
                Start Matching Now
                <ArrowRight className="ml-2 h-5 w-5 transition-transform group-hover:translate-x-1" />
              </Button>
            </Link>
            <a
              href="https://calendly.com/marita_ge/30min"
              target="_blank"
              rel="noopener noreferrer"
            >
              <Button 
                size="lg" 
                variant="outline" 
                className="h-12 border-2 border-border bg-background px-8 text-base font-semibold hover:bg-accent hover:border-primary/50"
              >
                Schedule Demo
                <ArrowRight className="ml-2 h-5 w-5 transition-transform group-hover:translate-x-1" />
              </Button>
            </a>
          </div>
          
          <div className="mt-24 grid grid-cols-1 gap-8 sm:grid-cols-3">
            <div className="text-center">
              <div className="text-5xl font-bold text-foreground sm:text-6xl">725+</div>
              <div className="mt-3 text-base text-muted-foreground font-medium">Active Investors</div>
            </div>
            <div className="text-center">
              <div className="text-5xl font-bold text-foreground sm:text-6xl">AI</div>
              <div className="mt-3 text-base text-muted-foreground font-medium">Semantic Matching</div>
            </div>
            <div className="text-center">
              <div className="text-5xl font-bold text-foreground sm:text-6xl">100%</div>
              <div className="mt-3 text-base text-muted-foreground font-medium">Direct Contacts</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
