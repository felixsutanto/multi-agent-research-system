import Link from "next/link"
import { Brain, Zap, Target, TrendingUp, ArrowRight, Sparkles } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Navbar } from "@/components/layout/Navbar"

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-purple-50/30 to-indigo-50/30 dark:from-slate-950 dark:via-purple-950/20 dark:to-indigo-950/20">
      <Navbar />

      {/* Hero Section */}
      <section className="relative overflow-hidden">
        {/* Gradient orbs */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute -top-40 -right-40 w-80 h-80 bg-purple-400 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob" />
          <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-indigo-400 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-2000" />
          <div className="absolute top-1/2 left-1/2 w-80 h-80 bg-pink-400 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-4000" />
        </div>

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 sm:py-32">
          <div className="text-center space-y-8">
            {/* Badge */}
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-purple-100 dark:bg-purple-950/50 border-2 border-purple-200 dark:border-purple-900">
              <Sparkles className="w-4 h-4 text-purple-600 dark:text-purple-400" />
              <span className="text-sm font-medium text-purple-600 dark:text-purple-400">
                AI-Powered Research Platform
              </span>
            </div>

            {/* Main Heading */}
            <h1 className="text-5xl sm:text-6xl md:text-7xl font-black tracking-tight">
              <span className="block text-foreground">Multi-Agent</span>
              <span className="block bg-gradient-to-r from-purple-600 via-indigo-600 to-blue-600 bg-clip-text text-transparent">
                Research System
              </span>
            </h1>

            {/* Description */}
            <p className="max-w-2xl mx-auto text-xl sm:text-2xl text-muted-foreground leading-relaxed">
              Watch AI agents collaborate in real-time to conduct comprehensive research,
              analyze data, and generate professional reports with citations.
            </p>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
              <Link href="/research">
                <Button
                  size="lg"
                  className="group bg-gradient-to-r from-purple-600 to-indigo-600 
                           hover:from-purple-700 hover:to-indigo-700 
                           px-8 h-14 text-lg rounded-xl shadow-xl 
                           hover:shadow-2xl transition-all duration-300"
                >
                  Start Research
                  <ArrowRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />
                </Button>
              </Link>
              <Link href="#features">
                <Button
                  variant="outline"
                  size="lg"
                  className="px-8 h-14 text-lg rounded-xl border-2"
                >
                  Learn More
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="relative py-24 bg-white/50 dark:bg-slate-900/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-foreground mb-4">
              Powered by Advanced AI Agents
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Our multi-agent system orchestrates specialized AI agents to deliver comprehensive research results
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <FeatureCard
              icon={Brain}
              title="Real-Time Streaming"
              description="Watch agents work together with live updates and streaming reports"
              gradient="from-purple-500 to-indigo-500"
            />
            <FeatureCard
              icon={Zap}
              title="Multi-Agent System"
              description="Planner, Researcher, Analyst, and Critic agents collaborate seamlessly"
              gradient="from-blue-500 to-cyan-500"
            />
            <FeatureCard
              icon={Target}
              title="Quality Metrics"
              description="RAG Triad scores ensure high-quality, grounded research outputs"
              gradient="from-green-500 to-emerald-500"
            />
            <FeatureCard
              icon={TrendingUp}
              title="Interactive Results"
              description="Explore reports with citations, charts, and downloadable formats"
              gradient="from-amber-500 to-orange-500"
            />
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="relative py-24">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="p-12 rounded-3xl bg-gradient-to-br from-purple-600 to-indigo-600 shadow-2xl">
            <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
              Ready to Transform Your Research?
            </h2>
            <p className="text-lg text-purple-100 mb-8 max-w-2xl mx-auto">
              Join researchers leveraging AI to conduct faster, more comprehensive research
            </p>
            <Link href="/research">
              <Button
                size="lg"
                variant="secondary"
                className="bg-white text-purple-600 hover:bg-purple-50 
                         px-8 h-14 text-lg rounded-xl shadow-xl 
                         hover:shadow-2xl transition-all"
              >
                Get Started Now
                <ArrowRight className="w-5 h-5 ml-2" />
              </Button>
            </Link>
          </div>
        </div>
      </section>
    </div>
  )
}

function FeatureCard({
  icon: Icon,
  title,
  description,
  gradient
}: {
  icon: React.ElementType
  title: string
  description: string
  gradient: string
}) {
  return (
    <div className="group relative p-6 rounded-2xl border-2 border-border 
                   bg-white dark:bg-slate-950 
                   hover:border-purple-300 dark:hover:border-purple-700 
                   hover:shadow-xl transition-all duration-300">
      <div className={`inline-flex p-3 rounded-xl bg-gradient-to-br ${gradient} mb-4`}>
        <Icon className="w-6 h-6 text-white" />
      </div>
      <h3 className="text-xl font-semibold text-foreground mb-2 group-hover:text-purple-600 dark:group-hover:text-purple-400 transition-colors">
        {title}
      </h3>
      <p className="text-muted-foreground leading-relaxed">
        {description}
      </p>
    </div>
  )
}
