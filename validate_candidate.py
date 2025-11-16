import sys
import os
sys.path.append('.')

from src.matcher import SimpleMatcher
import argparse

def validate_specific_candidate(candidate_name=None, output_file=None):
    matcher = SimpleMatcher()
    results, jobs, candidates = matcher.find_matches()
    
    output_lines = []
    
    if candidate_name:
        found_candidates = [c for c in candidates if candidate_name.lower() in c['name'].lower()]
        
        if not found_candidates:
            output_lines.append(f"❌ Candidate '{candidate_name}' not found.")
            output_lines.append(f"Available candidates: {[c['name'] for c in candidates]}")
        else:
            candidate = found_candidates[0]
            
            output_lines.append(f"👤 CANDIDATE: {candidate['name']}")
            output_lines.append("=" * 70)
            
            # Key candidate information only
            output_lines.append(f"📧 Email: {candidate.get('email', 'N/A')}")
            output_lines.append(f"📍 Location: {candidate.get('location', 'N/A')}")
            output_lines.append(f"💼 Experience: {candidate.get('experience_years', 0)} years")
            output_lines.append(f"🔧 Skills: {', '.join(candidate.get('skills', []))}")
            
            # Growth metrics - ALL dimensions
            growth = candidate.get('growth_metrics', {})
            if growth:
                output_lines.append(f"📈 Growth Score: {growth.get('growth_potential_score', 0)}%")
                dimensions = growth.get('growth_dimensions', {})
                if dimensions:
                    output_lines.append("   Growth Dimensions:")
                    output_lines.append(f"      - Vertical Growth: {(dimensions.get('vertical_growth', 0) * 100):.0f}%")
                    output_lines.append(f"      - Scope Growth: {(dimensions.get('scope_growth', 0) * 100):.0f}%")
                    output_lines.append(f"      - Impact Growth: {(dimensions.get('impact_growth', 0) * 100):.0f}%")
                    output_lines.append(f"      - Adaptability: {(dimensions.get('adaptability', 0) * 100):.0f}%")
                    output_lines.append(f"      - Leadership Velocity: {(dimensions.get('leadership_velocity', 0) * 100):.0f}%")
                
                output_lines.append("   Career Analysis:")
                output_lines.append(f"      - Career Archetype: {growth.get('career_archetype', 'N/A')}")
                output_lines.append(f"      - Career Stage: {growth.get('career_stage', 'N/A')}")
                output_lines.append(f"      - Executive Potential: {(growth.get('executive_potential', 0) * 100):.0f}%")
                output_lines.append(f"      - Strategic Mobility: {(growth.get('strategic_mobility', 0) * 100):.0f}%")
                output_lines.append(f"      - Analysis: {growth.get('analysis_rationale', 'N/A')}")
            
            output_lines.append("")
            output_lines.append("🎯 JOB MATCHES (Sorted by Best Match)")
            output_lines.append("=" * 70)
            
            # Collect and sort matches
            candidate_matches = []
            for job_index, job_matches in results.items():
                for match in job_matches:
                    if match['candidate']['name'].lower() == candidate['name'].lower():
                        candidate_matches.append((jobs[job_index], match))
            
            # Sort by score (highest first)
            candidate_matches.sort(key=lambda x: x[1]['score'], reverse=True)
            
            if candidate_matches:
                for job, match in candidate_matches:
                    score_percent = (match.get('score', 0) * 100)
                    output_lines.append(f"🏢 {job['title']} at {job.get('company', 'N/A')}")
                    output_lines.append(f"📊 Overall Match Score: {score_percent:.1f}% ({match.get('match_grade', 'N/A')})")
                    
                    # Score Breakdown
                    breakdown = match.get('score_breakdown', {})
                    if breakdown:
                        output_lines.append("   Score Breakdown:")
                        output_lines.append(f"      - Skills Match: {breakdown.get('skills', 0)}%")
                        output_lines.append(f"      - Experience: {breakdown.get('experience', 0)}%")
                        output_lines.append(f"      - Location: {breakdown.get('location', 0)}%")
                        output_lines.append(f"      - Profile Relevance: {breakdown.get('semantic', 0)}%")
                        output_lines.append(f"      - Cultural Fit: {breakdown.get('cultural_fit', 0)}%")
                    
                    # Cultural Fit Breakdown
                    cultural_breakdown = match.get('cultural_breakdown', {})
                    if cultural_breakdown:
                        output_lines.append("   Cultural Fit Breakdown:")
                        output_lines.append(f"      - Keyword Score: {cultural_breakdown.get('keyword_score', 0)}%")
                        output_lines.append(f"      - Semantic Score: {cultural_breakdown.get('semantic_score', 0)}%")
                        output_lines.append(f"      - Final Score: {cultural_breakdown.get('final_score', 0)}%")
                    
                    # Growth Breakdown
                    growth_breakdown = match.get('growth_breakdown', {})
                    if growth_breakdown:
                        output_lines.append("   Growth Breakdown:")
                        output_lines.append(f"      - Growth Potential: {match.get('growth_potential_score', 0)}%")
                        output_lines.append(f"      - Vertical Growth: {(growth_breakdown.get('vertical_growth', 0) * 100):.0f}%")
                        output_lines.append(f"      - Scope Growth: {(growth_breakdown.get('scope_growth', 0) * 100):.0f}%")
                        output_lines.append(f"      - Impact Growth: {(growth_breakdown.get('impact_growth', 0) * 100):.0f}%")
                        output_lines.append(f"      - Adaptability: {(growth_breakdown.get('adaptability', 0) * 100):.0f}%")
                        output_lines.append(f"      - Leadership Velocity: {(growth_breakdown.get('leadership_velocity', 0) * 100):.0f}%")
                        output_lines.append(f"      - Career Archetype: {growth_breakdown.get('career_archetype', 'N/A')}")
                        output_lines.append(f"      - Career Stage: {growth_breakdown.get('career_stage', 'N/A')}")
                        output_lines.append(f"      - Executive Potential: {(growth_breakdown.get('executive_potential', 0) * 100):.0f}%")
                        output_lines.append(f"      - Strategic Mobility: {(growth_breakdown.get('strategic_mobility', 0) * 100):.0f}%")
                    
                    common_skills = match.get('common_skills', [])
                    if common_skills:
                        output_lines.append(f"   🔗 Common Skills: {', '.join(common_skills)}")
                    
                    output_lines.append("")
            else:
                output_lines.append(f"❌ No matches found for {candidate_name}")
    else:
        # Show all candidates summary
        output_lines.append("📊 CANDIDATES SUMMARY")
        output_lines.append("=" * 70)
        for candidate in candidates:
            growth = candidate.get('growth_metrics', {})
            growth_score = growth.get('growth_potential_score', 0) if growth else 0
            output_lines.append(f"👤 {candidate['name']:20} | 📈 Growth: {growth_score:5.1f}% | 💼 Exp: {candidate.get('experience_years', 0):2} years | 📧 {candidate.get('email', 'N/A')}")
    
    # Output to file or console
    output_text = '\n'.join(output_lines)
    
    if output_file:
        with open(output_file, 'w') as f:
            f.write(output_text)
        print(f"✅ Output saved to: {output_file}")
    else:
        print(output_text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Validate candidate metrics')
    parser.add_argument('--name', type=str, help='Candidate name to search for (partial match supported)')
    parser.add_argument('--output', '-o', type=str, help='Output file to save results')
    
    args = parser.parse_args()
    validate_specific_candidate(args.name, args.output)
