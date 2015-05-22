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

import java.io.Serializable;
import java.util.UUID;

import javax.persistence.Column;
import javax.persistence.Embeddable;
import javax.persistence.Lob;

import org.hibernate.annotations.Type;

@Embeddable
public class MetricDimensionDbId implements Serializable {

  @Column(name = "dimension_set_id", length = 20)
  @Lob
  @Type(type = "org.hibernate.type.UUIDBinaryType")
  private UUID dimension_set_id;

  @Column(name = "name", length = 255, nullable = false)
  private String name;

  @Column(name = "value", length = 255, nullable = false)
  private String value;

  public MetricDimensionDbId() {
    this(DbUtils.toUUID(DbUtils.DEFAULT_VALUE), "", "");
  }

  public MetricDimensionDbId(UUID dimension_set_id, String name, String value) {
    super();
    this.dimension_set_id = dimension_set_id;
    this.name = name;
    this.value = value;
  }

  public MetricDimensionDbId(byte[] dimension_set_id, String name, String value) {
    this(DbUtils.toUUID(dimension_set_id), name, value);
  }

  public byte[] getDimension_set_id() {
    return DbUtils.toByteArray(dimension_set_id);
  }

  public void setDimension_set_id(byte[] dimension_set_id) {
    this.dimension_set_id = DbUtils.toUUID(dimension_set_id);
  }

  public String getName() {
    return name;
  }

  public void setName(String name) {
    this.name = name;
  }

  public String getValue() {
    return value;
  }

  public void setValue(String value) {
    this.value = value;
  }

  public void setDimension_set_id(UUID dimension_set_id) {
    this.dimension_set_id = dimension_set_id;
  }

  @Override
  public int hashCode() {
    final int prime = 31;
    int result = 1;
    result = prime * result + ((dimension_set_id == null) ? 0 : dimension_set_id.hashCode());
    result = prime * result + ((name == null) ? 0 : name.hashCode());
    result = prime * result + ((value == null) ? 0 : value.hashCode());
    return result;
  }

  @Override
  public boolean equals(Object obj) {
    if (this == obj)
      return true;
    if (obj == null)
      return false;
    if (getClass() != obj.getClass())
      return false;
    MetricDimensionDbId other = (MetricDimensionDbId) obj;
    if (dimension_set_id == null) {
      if (other.dimension_set_id != null)
        return false;
    } else if (!dimension_set_id.equals(other.dimension_set_id))
      return false;
    if (name == null) {
      if (other.name != null)
        return false;
    } else if (!name.equals(other.name))
      return false;
    if (value == null) {
      if (other.value != null)
        return false;
    } else if (!value.equals(other.value))
      return false;
    return true;
  }
}
