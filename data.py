import os
import csv
import random
import numpy as np
from dotenv import load_dotenv
import openai
from tqdm import tqdm

# Load environment variables
load_dotenv()

# Set up OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

# Product categories
PRODUCTS = [
    "Construction Coverall", "Factory Lab Coat", "Mechanic Jumpsuit", "Welding Apron",
    "Industrial Work Shirt", "Cabin Crew Jacket", "Security Guard Blazer", "Chef Coat",
    "Paramedic Scrubs", "Police Patrol Shirt", "Hiking Shell Jacket", "Tactical Cargo Pants",
    "Waterproof Parka", "Insulated Camping Vest", "Trail Running Shorts", "Compression Tights",
    "Training Tracksuit", "Athletic Performance Tee", "Yoga Leggings", "Running Windbreaker",
    "Steel Toe Boots", "Slip-Resistant Clogs", "Waterproof Hiking Boots", "Lightweight Running Shoes",
    "High-Top Basketball Sneakers"
]

# Create default base values for each product
def get_product_base_values():
    print("Using predefined values for product metrics")
    base_values = {}
    
    # Create detailed default values for each product type
    for product in PRODUCTS:
        # Workwear category
        if product == "Construction Coverall":
            base_values[product] = {
                "raw_material": 2.8, "weaving": 4.5, "dyeing": 6.2, 
                "finishing": 920, "energy_used": 19.5, "water_used": 1200, "co2_used": 12.5
            }
        elif product == "Factory Lab Coat":
            base_values[product] = {
                "raw_material": 1.9, "weaving": 3.7, "dyeing": 5.1, 
                "finishing": 780, "energy_used": 16.2, "water_used": 980, "co2_used": 9.2
            }
        elif product == "Mechanic Jumpsuit":
            base_values[product] = {
                "raw_material": 2.6, "weaving": 4.3, "dyeing": 5.8, 
                "finishing": 880, "energy_used": 18.5, "water_used": 1150, "co2_used": 11.8
            }
        elif product == "Welding Apron":
            base_values[product] = {
                "raw_material": 2.2, "weaving": 3.4, "dyeing": 4.2, 
                "finishing": 650, "energy_used": 14.8, "water_used": 820, "co2_used": 9.8
            }
        elif product == "Industrial Work Shirt":
            base_values[product] = {
                "raw_material": 1.6, "weaving": 3.0, "dyeing": 4.5, 
                "finishing": 620, "energy_used": 13.5, "water_used": 780, "co2_used": 8.5
            }
        # Professional uniforms
        elif product == "Cabin Crew Jacket":
            base_values[product] = {
                "raw_material": 2.0, "weaving": 4.0, "dyeing": 5.0, 
                "finishing": 828, "energy_used": 17.0, "water_used": 1028, "co2_used": 10.0
            }
        elif product == "Security Guard Blazer":
            base_values[product] = {
                "raw_material": 2.1, "weaving": 4.1, "dyeing": 5.2, 
                "finishing": 840, "energy_used": 17.4, "water_used": 1050, "co2_used": 10.3
            }
        elif product == "Chef Coat":
            base_values[product] = {
                "raw_material": 1.8, "weaving": 3.6, "dyeing": 4.8, 
                "finishing": 750, "energy_used": 15.8, "water_used": 950, "co2_used": 9.1
            }
        elif product == "Paramedic Scrubs":
            base_values[product] = {
                "raw_material": 1.5, "weaving": 2.8, "dyeing": 4.3, 
                "finishing": 680, "energy_used": 13.2, "water_used": 820, "co2_used": 7.9
            }
        elif product == "Police Patrol Shirt":
            base_values[product] = {
                "raw_material": 1.7, "weaving": 3.2, "dyeing": 4.5, 
                "finishing": 700, "energy_used": 14.5, "water_used": 880, "co2_used": 8.7
            }
        # Outdoor apparel  
        elif product == "Hiking Shell Jacket":
            base_values[product] = {
                "raw_material": 2.3, "weaving": 3.8, "dyeing": 5.5, 
                "finishing": 950, "energy_used": 18.0, "water_used": 1100, "co2_used": 10.8
            }
        elif product == "Tactical Cargo Pants":
            base_values[product] = {
                "raw_material": 2.1, "weaving": 3.9, "dyeing": 5.2, 
                "finishing": 880, "energy_used": 17.2, "water_used": 1050, "co2_used": 10.5
            }
        elif product == "Waterproof Parka":
            base_values[product] = {
                "raw_material": 2.9, "weaving": 4.6, "dyeing": 6.5, 
                "finishing": 1050, "energy_used": 21.5, "water_used": 1250, "co2_used": 13.2
            }
        elif product == "Insulated Camping Vest":
            base_values[product] = {
                "raw_material": 1.9, "weaving": 3.2, "dyeing": 4.8, 
                "finishing": 820, "energy_used": 16.8, "water_used": 950, "co2_used": 9.5
            }
        elif product == "Trail Running Shorts":
            base_values[product] = {
                "raw_material": 1.1, "weaving": 2.3, "dyeing": 3.7, 
                "finishing": 580, "energy_used": 11.5, "water_used": 650, "co2_used": 6.8
            }
        # Athletic wear
        elif product == "Compression Tights":
            base_values[product] = {
                "raw_material": 1.3, "weaving": 2.8, "dyeing": 4.0, 
                "finishing": 620, "energy_used": 12.8, "water_used": 750, "co2_used": 7.5
            }
        elif product == "Training Tracksuit":
            base_values[product] = {
                "raw_material": 2.4, "weaving": 4.2, "dyeing": 5.7, 
                "finishing": 920, "energy_used": 18.5, "water_used": 1150, "co2_used": 11.0
            }
        elif product == "Athletic Performance Tee":
            base_values[product] = {
                "raw_material": 1.2, "weaving": 2.5, "dyeing": 3.8, 
                "finishing": 550, "energy_used": 12.0, "water_used": 680, "co2_used": 6.9
            }
        elif product == "Yoga Leggings":
            base_values[product] = {
                "raw_material": 1.4, "weaving": 2.7, "dyeing": 3.9, 
                "finishing": 580, "energy_used": 12.5, "water_used": 700, "co2_used": 7.2
            }
        elif product == "Running Windbreaker":
            base_values[product] = {
                "raw_material": 1.7, "weaving": 3.1, "dyeing": 4.2, 
                "finishing": 700, "energy_used": 14.8, "water_used": 850, "co2_used": 8.3
            }
        # Footwear
        elif product == "Steel Toe Boots":
            base_values[product] = {
                "raw_material": 3.2, "weaving": 2.0, "dyeing": 4.5, 
                "finishing": 650, "energy_used": 23.5, "water_used": 780, "co2_used": 14.5
            }
        elif product == "Slip-Resistant Clogs":
            base_values[product] = {
                "raw_material": 2.5, "weaving": 1.6, "dyeing": 3.8, 
                "finishing": 580, "energy_used": 18.2, "water_used": 650, "co2_used": 12.0
            }
        elif product == "Waterproof Hiking Boots":
            base_values[product] = {
                "raw_material": 3.0, "weaving": 1.9, "dyeing": 4.2, 
                "finishing": 620, "energy_used": 21.8, "water_used": 750, "co2_used": 13.5
            }
        elif product == "Lightweight Running Shoes":
            base_values[product] = {
                "raw_material": 2.3, "weaving": 1.5, "dyeing": 3.6, 
                "finishing": 520, "energy_used": 17.5, "water_used": 600, "co2_used": 11.2
            }
        elif product == "High-Top Basketball Sneakers":
            base_values[product] = {
                "raw_material": 2.7, "weaving": 1.7, "dyeing": 4.0, 
                "finishing": 580, "energy_used": 19.5, "water_used": 680, "co2_used": 12.8
            }
    
    return base_values

# Function to determine sustainability grade based on metrics
def calculate_sustainability_grade(raw_material, weaving, dyeing, finishing, energy_used, water_used, co2_used):
    # Calculate environmental impact score (lower is better)
    # This is a simplified model - in reality more complex models would be used
    
    # Normalize each metric to a 0-1 scale based on typical ranges
    normalized_raw = raw_material / 5.0  # Assuming 0-5kg CO2 range
    normalized_weaving = weaving / 8.0   # Assuming 0-8kg CO2 range
    normalized_dyeing = dyeing / 10.0    # Assuming 0-10kWh range
    normalized_finishing = finishing / 1500.0  # Assuming 0-1500L H2O range
    normalized_energy = energy_used / 30.0     # Assuming 0-30kWh range
    normalized_water = water_used / 2000.0     # Assuming 0-2000L range
    normalized_co2 = co2_used / 20.0     # Assuming 0-20kg CO2 range
    
    # Calculate total environmental impact (weighted average)
    impact_score = (
        normalized_raw * 0.15 + 
        normalized_weaving * 0.1 + 
        normalized_dyeing * 0.1 + 
        normalized_finishing * 0.15 + 
        normalized_energy * 0.2 + 
        normalized_water * 0.15 + 
        normalized_co2 * 0.15
    )
    
    # Assign grade
    if impact_score < 0.3:
        return "A"
    elif impact_score < 0.5:
        return "B"
    elif impact_score < 0.7:
        return "C"
    else:
        return "D"

# Main function to generate the dataset
def generate_synthetic_dataset(num_samples=1000, filename="synthetic_sustainability_dataset.csv"):
    # Get base values for each product
    print("Getting base values for products...")
    base_values = get_product_base_values()
    
    # Prepare to write the data to a CSV file
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = [
            'Product', 'Raw Material (kg CO2)', 'Weaving (kg CO2)', 
            'Dyeing (kWh)', 'Finishing (Litres H2O)', 'Energy Used (kWh)',
            'Water Used (Litres)', 'CO2 Used (kg)', 'Sustainability Grade'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        # Ensure all grades (A, B, C, D) are represented
        grade_distribution = {"A": 0.1, "B": 0.4, "C": 0.3, "D": 0.2}  # Target distribution
        grade_counts = {"A": 0, "B": 0, "C": 0, "D": 0}
        target_counts = {grade: int(num_samples * pct) for grade, pct in grade_distribution.items()}
        
        # Adjust the last grade to ensure we get exactly num_samples
        total = sum(target_counts.values())
        if total < num_samples:
            target_counts["B"] += (num_samples - total)  # Add remaining to B grade
        
        samples_created = 0
        attempts = 0
        max_attempts = num_samples * 10  # Limit attempts to avoid infinite loops
        
        print(f"Generating {num_samples} synthetic samples with varied grade distribution...")
        with tqdm(total=num_samples) as pbar:
            while samples_created < num_samples and attempts < max_attempts:
                attempts += 1
                
                # Randomly select a product
                product = random.choice(PRODUCTS)
                
                # Get base values for this product
                base = base_values[product]  # We're sure all products are in the dictionary
                
                # Add random variations with different ranges depending on what grade we need more of
                variation_ranges = {
                    "A": (0.5, 0.8),   # Lower impact for A grade
                    "B": (0.8, 1.0),   # Slightly lower for B grade
                    "C": (1.0, 1.2),   # Slightly higher for C grade
                    "D": (1.2, 1.5)    # Higher impact for D grade
                }
                
                # Decide which grade we're targeting with this sample
                # Prioritize grades that are under their target count
                remaining = {g: target_counts[g] - grade_counts[g] for g in grade_counts}
                available_grades = [g for g, r in remaining.items() if r > 0]
                
                if not available_grades:  # All targets met
                    break
                    
                target_grade = random.choice(available_grades)
                variation_range = variation_ranges[target_grade]
                
                # Generate values with appropriate variation
                raw_material = max(0.1, base["raw_material"] * random.uniform(*variation_range))
                weaving = max(0.1, base["weaving"] * random.uniform(*variation_range))
                dyeing = max(0.1, base["dyeing"] * random.uniform(*variation_range))
                finishing = max(10, base["finishing"] * random.uniform(*variation_range))
                energy_used = max(1, base["energy_used"] * random.uniform(*variation_range))
                water_used = max(10, base["water_used"] * random.uniform(*variation_range))
                co2_used = max(0.1, base["co2_used"] * random.uniform(*variation_range))
                
                # Calculate sustainability grade
                grade = calculate_sustainability_grade(
                    raw_material, weaving, dyeing, finishing, 
                    energy_used, water_used, co2_used
                )
                
                # If this sample's grade matches what we need, add it to the dataset
                if grade == target_grade and grade_counts[grade] < target_counts[grade]:
                    # Round values to appropriate precision
                    raw_material = round(raw_material, 1)
                    weaving = round(weaving, 1)
                    dyeing = round(dyeing, 1)
                    finishing = round(finishing)
                    energy_used = round(energy_used, 1)
                    water_used = round(water_used)
                    co2_used = round(co2_used, 1)
                    
                    # Write to CSV
                    writer.writerow({
                        'Product': product,
                        'Raw Material (kg CO2)': raw_material,
                        'Weaving (kg CO2)': weaving,
                        'Dyeing (kWh)': dyeing,
                        'Finishing (Litres H2O)': finishing,
                        'Energy Used (kWh)': energy_used,
                        'Water Used (Litres)': water_used,
                        'CO2 Used (kg)': co2_used,
                        'Sustainability Grade': grade
                    })
                    
                    grade_counts[grade] += 1
                    samples_created += 1
                    pbar.update(1)
        
    print(f"\nDataset generated and saved to {filename}")
    print(f"Generated {samples_created} samples after {attempts} attempts")
    
    # Generate some basic statistics about the dataset
    print("\nDataset Statistics:")
    try:
        import pandas as pd
        df = pd.read_csv(filename)
        grade_counts = df['Sustainability Grade'].value_counts()
        print(f"Grade distribution: {grade_counts.to_dict()}")
        print(f"Number of unique products: {df['Product'].nunique()}")
        
        # Print average values by product type
        print("\nSample metrics by product type:")
        print(df.groupby('Product')['CO2 Used (kg)'].mean().sort_values(ascending=False).head(5))
    except ImportError:
        print("Grade distribution:", grade_counts)
        print("Install pandas to see more detailed dataset statistics")

if __name__ == "__main__":
    generate_synthetic_dataset(1000)