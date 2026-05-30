import ThemeToggle from "@/components/ThemeToggle";
import UploadTrace from '@/components/UploadTrace';
const page = () => {
  return (
    <main className="min-h-screen bg-zinc-50 p-8 text-zinc-900 dark:bg-zinc-950 dark:text-zinc-100">
      <div className="mx-auto max-w-6xl">
      <div className="mb-6 flex justify-end">
            <ThemeToggle />
          </div>
        <h1 className="text-4xl font-bold">
          Agent Trace Analyzer
        </h1>

        <UploadTrace />
      </div>
    </main>
  )
}

export default page