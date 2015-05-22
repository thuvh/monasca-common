/*
 * Copyright 2015 FUJITSU LIMITED
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
 * in compliance with the License. You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software distributed under the License
 * is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
 * or implied. See the License for the specific language governing permissions and limitations under
 * the License.
 */
package monasca.common.hibernate.db;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;

import org.joda.time.DateTime;

@Entity
@Table(name = "sub_alarm_definition")
public class SubAlarmDefinitionDb extends CreateUpdateDate{

  @Id
  @Column(name = "id", length = 36)
  private String id;

  @Column(name = "alarm_definition_id", length = 36, nullable = false)
  private String alarm_definition_id;

  @Column(name = "function", length = 10, nullable = false)
  private String function;

  @Column(name = "metric_name", length = 100, nullable = true)
  private String metric_name;

  @Column(name = "operator", length = 5, nullable = false)
  private String operator;

  @Column(name = "threshold", nullable = false)
  private Double threshold;

  @Column(name = "period", length = 11, nullable = false)
  private Integer period;

  @Column(name = "periods", length = 11, nullable = false)
  private Integer periods;

  public SubAlarmDefinitionDb() {
    super();
  }

  public SubAlarmDefinitionDb(String id, String alarm_definition_id, String function, String metric_name, String operator, Double threshold,
      Integer period, Integer periods, DateTime created_at, DateTime updated_at) {
    super(created_at, updated_at);
    this.id = id;
    this.alarm_definition_id = alarm_definition_id;
    this.function = function;
    this.metric_name = metric_name;
    this.operator = operator;
    this.threshold = threshold;
    this.period = period;
    this.periods = periods;
  }

  public String getId() {
    return id;
  }

  public void setId(String id) {
    this.id = id;
  }

  public String getAlarm_definition_id() {
    return alarm_definition_id;
  }

  public void setAlarm_definition_id(String alarm_definition_id) {
    this.alarm_definition_id = alarm_definition_id;
  }

  public String getFunction() {
    return function;
  }

  public void setFunction(String function) {
    this.function = function;
  }

  public String getMetric_name() {
    return metric_name;
  }

  public void setMetric_name(String metric_name) {
    this.metric_name = metric_name;
  }

  public String getOperator() {
    return operator;
  }

  public void setOperator(String operator) {
    this.operator = operator;
  }

  public Double getThreshold() {
    return threshold;
  }

  public void setThreshold(Double threshold) {
    this.threshold = threshold;
  }

  public Integer getPeriod() {
    return period;
  }

  public void setPeriod(Integer period) {
    this.period = period;
  }

  public Integer getPeriods() {
    return periods;
  }

  public void setPeriods(Integer periods) {
    this.periods = periods;
  }
}
