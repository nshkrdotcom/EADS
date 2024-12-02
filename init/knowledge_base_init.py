from neo4j import GraphDatabase
import json
import os
import logging
from typing import List, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KnowledgeBaseInitializer:
    def __init__(self):
        self.neo4j_uri = os.getenv('NEO4J_URI', 'bolt://neo4j:7687')
        self.neo4j_user = os.getenv('NEO4J_USER', 'neo4j')
        self.neo4j_password = os.getenv('NEO4J_PASSWORD', 'password')
        
    def load_base_patterns(self) -> List[Dict]:
        """Load base design patterns from JSON file"""
        patterns_file = os.path.join(os.path.dirname(__file__), 'data/base_patterns.json')
        try:
            with open(patterns_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Base patterns file not found at {patterns_file}")
            return []

    def init_knowledge_base(self):
        """Initialize knowledge base with design patterns and relationships"""
        try:
            driver = GraphDatabase.driver(
                self.neo4j_uri,
                auth=(self.neo4j_user, self.neo4j_password)
            )

            patterns = self.load_base_patterns()
            
            with driver.session() as session:
                # Create pattern categories
                session.run("""
                    MERGE (c:Category {name: 'Creational'})
                    MERGE (c:Category {name: 'Structural'})
                    MERGE (c:Category {name: 'Behavioral'})
                """)
                
                # Create base knowledge structure
                for pattern in patterns:
                    session.run("""
                        MATCH (cat:Category {name: $category})
                        MERGE (p:Pattern {
                            name: $name,
                            description: $description
                        })
                        MERGE (p)-[:BELONGS_TO]->(cat)
                        WITH p
                        UNWIND $use_cases as use_case
                        MERGE (u:UseCase {description: use_case})
                        MERGE (p)-[:APPLIES_TO]->(u)
                    """, pattern)
                
                # Create relationships between patterns
                session.run("""
                    MATCH (p1:Pattern)
                    MATCH (p2:Pattern)
                    WHERE p1 <> p2
                    AND p1.category = p2.category
                    MERGE (p1)-[:RELATED_TO]->(p2)
                """)
                
            logger.info("Knowledge base initialization completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error initializing knowledge base: {str(e)}")
            return False
        finally:
            if 'driver' in locals():
                driver.close()

def main():
    initializer = KnowledgeBaseInitializer()
    success = initializer.init_knowledge_base()
    
    if success:
        logger.info("Knowledge base initialization completed successfully")
    else:
        logger.error("Knowledge base initialization failed")

if __name__ == "__main__":
    main()
