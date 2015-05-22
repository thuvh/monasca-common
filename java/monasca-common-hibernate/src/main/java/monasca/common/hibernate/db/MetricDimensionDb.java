/*
 * Copyright (c) 2014 Hewlett-Packard Development Company, L.P.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
 * implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package monasca.common.hibernate.db;

import javax.persistence.EmbeddedId;
import javax.persistence.Entity;
import javax.persistence.Table;

@Entity
@Table(name = "metric_dimension")
public class MetricDimensionDb {

  @EmbeddedId
  private MetricDimensionDbId id;

  public MetricDimensionDb() {
    super();
  }

  public MetricDimensionDb(MetricDimensionDbId id) {
    super();
    this.id = id;
  }

  public MetricDimensionDb(byte[] dimension_set_id, String name, String value) {
    super();
    this.id = new MetricDimensionDbId(dimension_set_id, name, value);
  }

  public MetricDimensionDbId getId() {
    return id;
  }

  public void setId(MetricDimensionDbId id) {
    this.id = id;
  }
}
