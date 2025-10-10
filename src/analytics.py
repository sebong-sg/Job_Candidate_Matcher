# 📈 ANALYTICS & REPORT GENERATOR
# Shows insights about your matching data

from database import DataManager
from matcher import SimpleMatcher
import json
from datetime import datetime

class Analytics:
    def __init__(self):
        self.db = DataManager()
        self.matcher = SimpleMatcher()
    
    def generate_report(self):
        """Generate a comprehensive analytics report"""
        print("\n" + "📊" * 25)
        print("📈 ANALYTICS REPORT")
        print("📊" * 25)
        
        jobs = self.db.load_jobs()
        candidates = self.db.load_candidates()
        
        # Basic stats
        print(f"\n📋 BASIC STATS:")
        print(f"   • Total Jobs: {len(jobs)}")
        print(f"   • Total Candidates: {len(candidates)}")
        print(f"   • Candidate/Job Ratio: {len(candidates)/len(jobs):.1f}:1")
        
        # Skill analysis
        print(f"\n🔧 SKILL ANALYSIS:")
        all_job_skills = []
        all_candidate_skills = []
        
        for job in jobs:
            all_job_skills.extend(job['required_skills'])
        
        for candidate in candidates:
            all_candidate_skills.extend(candidate['skills'])
        
        # Most demanded skills
        from collections import Counter
        job_skill_counts = Counter(all_job_skills)
        candidate_skill_counts = Counter(all_candidate_skills)
        
        print(f"   🏆 Top 5 Most Demanded Skills:")
        for skill, count in job_skill_counts.most_common(5):
            print(f"      {skill}: {count} jobs")
        
        print(f"   👥 Top 5 Candidate Skills:")
        for skill, count in candidate_skill_counts.most_common(5):
            print(f"      {skill}: {count} candidates")
        
        # Location analysis
        print(f"\n📍 LOCATION ANALYSIS:")
        job_locations = Counter([job['location'] for job in jobs])
        candidate_locations = Counter([candidate['location'] for candidate in candidates])
        
        print(f"   🏢 Job Locations:")
        for location, count in job_locations.most_common(3):
            print(f"      {location}: {count} jobs")
        
        print(f"   👤 Candidate Locations:")  
        for location, count in candidate_locations.most_common(3):
            print(f"      {location}: {count} candidates")
        
        # Experience analysis
        print(f"\n🎯 EXPERIENCE ANALYSIS:")
        experience_levels = [candidate['experience_years'] for candidate in candidates]
        avg_experience = sum(experience_levels) / len(experience_levels) if experience_levels else 0
        
        print(f"   • Average Candidate Experience: {avg_experience:.1f} years")
        print(f"   • Most Experienced: {max(experience_levels) if experience_levels else 0} years")
        print(f"   • Least Experienced: {min(experience_levels) if experience_levels else 0} years")
        
        # Generate matching insights
        print(f"\n🤖 MATCHING INSIGHTS:")
        results, jobs, candidates = self.matcher.find_matches()
        
        total_matches = 0
        high_quality_matches = 0
        
        for job_index, job_matches in results.items():
            total_matches += len(job_matches)
            high_quality_matches += len([m for m in job_matches if m['score'] > 0.5])
        
        print(f"   • Total Matches Found: {total_matches}")
        print(f"   • High-Quality Matches (>0.5): {high_quality_matches}")
        print(f"   • Match Rate: {(total_matches/len(jobs)):.1f} matches per job")
        
        # Skill gaps
        print(f"\n⚠️  SKILL GAPS IDENTIFIED:")
        missing_skills = set(all_job_skills) - set(all_candidate_skills)
        if missing_skills:
            for skill in list(missing_skills)[:5]:  # Show top 5 missing skills
                print(f"   • {skill}: In demand but no candidates have it")
        else:
            print("   ✅ No major skill gaps found!")
        
        print("\n" + "="*60)
        print("📋 REPORT GENERATED:", datetime.now().strftime("%Y-%m-%d %H:%M"))
        print("="*60)

def main():
    """Run analytics report"""
    analytics = Analytics()
    analytics.generate_report()

if __name__ == "__main__":
    main()