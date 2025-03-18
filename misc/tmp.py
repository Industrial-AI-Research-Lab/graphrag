import asyncio
import json
from elasticsearch import AsyncElasticsearch
import logging
from tqdm.asyncio import tqdm

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

index_name = "9e4f0121-b7c4-4087-9995-4af351c58ef5"

async def export_elasticsearch_data(index_name, output_file, batch_size=1000):
    """
    Export all data from Elasticsearch index to a file using async API.
    
    Args:
        index_name: Name of the Elasticsearch index
        output_file: Path to output file
        batch_size: Number of documents to retrieve per batch
    """
    # Connect to Elasticsearch
    client = AsyncElasticsearch(hosts=["http://localhost:9200"])  # Update with your ES connection details
    
    try:
        # Get total document count for progress tracking
        count_resp = await client.count(index=index_name)
        total_docs = count_resp["count"]
        logger.info(f"Exporting {total_docs} documents from index '{index_name}'")
        
        # Initialize scroll
        resp = await client.search(
            index=index_name,
            scroll="5m",  # Keep the search context alive for 5 minutes
            size=batch_size,
            body={"query": {"match_all": {}}}
        )
        
        scroll_id = resp["_scroll_id"]
        hits = resp["hits"]["hits"]
        
        # Write to file
        with open(output_file, "w") as f:
            # Process initial batch
            for doc in hits:
                f.write(json.dumps(doc) + "\n")
            
            # Process remaining batches with progress bar
            with tqdm(total=total_docs, initial=len(hits)) as pbar:
                while len(hits) > 0:
                    # Get next batch of results
                    resp = await client.scroll(
                        scroll_id=scroll_id,
                        scroll="5m"
                    )
                    
                    # Update scroll_id
                    scroll_id = resp["_scroll_id"]
                    hits = resp["hits"]["hits"]
                    
                    # Write batch to file
                    for doc in hits:
                        f.write(json.dumps(doc) + "\n")
                    
                    # Update progress bar
                    pbar.update(len(hits))
        
        logger.info(f"Export completed successfully. Data saved to {output_file}")
    
    except Exception as e:
        logger.error(f"Error exporting data: {str(e)}")
        raise
    
    finally:
        # Clear the scroll context to free resources
        if 'scroll_id' in locals() and scroll_id:
            await client.clear_scroll(scroll_id=scroll_id)
        
        # Close the client
        await client.close()

async def main():
    output_file = f"{index_name}_export.jsonl"
    await export_elasticsearch_data(index_name, output_file)

if __name__ == "__main__":
    asyncio.run(main())